import contextlib
import pathlib
import subprocess
import time

import xml.etree.ElementTree as xml

import libvirt  # libvirt-python


@contextlib.contextmanager
def libvirt_connection(name='qemu:///session'):
    """Libvirt connection context."""
    conn = libvirt.open(name)
    try:
        yield conn
    finally:
        conn.close()


def domain(conn, name):
    """Return libvirt domain object or None if not defined."""
    if name in conn.listDefinedDomains():
        return conn.lookupByName(name)


def shutdown_domain(domain):
    """Shutdown the domain, trying several times before giving up."""
    domain.shutdown()
    start = time.time()
    timeout = 3 * 60  # 3 minutes
    while (time.time() - start) < timeout:
        state, reason = domain.state()
        if state == libvirt.VIR_DOMAIN_SHUTOFF:
            break
        else:
            time.sleep(1)
    if state != libvirt.VIR_DOMAIN_SHUTOFF:
        raise RuntimeError(f'shutdown of {domain} unsuccessful, currently: {state}')


def ensure_shutdown(domain, shutdown=True):
    """Raise exception if domain is not or can not be shutdown."""
    state, reason = domain.state()
    if state == libvirt.VIR_DOMAIN_RUNNING:
        if shutdown:
            shutdown_domain(domain)
        else:
            raise RuntimeError(f'domain {source} must be shut down')
    state, reason = domain.state()
    if state != libvirt.VIR_DOMAIN_SHUTOFF:
        msg = f'domain {source} must be shut down, current state: {state}'
        raise RuntimeError(msg)


def list_cow_disks(domain):
    """Return a list of copy-on-write disks (qcow2) used by this domain."""
    result = []
    for disk in domain.findall('devices/disk'):
        if disk.get('type') == 'file' and disk.get('device') == 'disk':
            driver = disk.find('driver')
            if driver.get('name') == 'qemu' and driver.get('type') == 'qcow2':
                source_file = pathlib.Path(disk.find('source').get('file'))
                target_dev = disk.find('target').get('dev')
                result.append((source_file, target_dev, disk))
    return result


def create_linked_clone(
    source, target, connection='qemu:///session', shutdown_source=True
):
    with libvirt_connection(connection) as conn:
        source_domain = domain(conn, source)
        if source_domain is None:
            raise ValueError(f'source libvirt domain {source} not found')
        if domain(conn, target) is not None:
            raise ValueError(f'target libvirt domain {target} already exists')
        domain_xml = xml.fromstring(source_domain.XMLDesc(0))
        cow_disks = list_cow_disks(domain_xml)
        if not cow_disks:
            msg = f'source libvirt domain {source} has no copy-on-write disks'
            raise ValueError(msg)
        ensure_shutdown(source_domain, shutdown_source)

        # set disks to readonly on source domain
        for _, _, disk_xml in cow_disks:
            readonly_tags = disk_xml.findall('readonly')
            if not readonly_tags:
                disk_xml.append(xml.Element('readonly'))
                disk_xml_str = xml.tostring(disk_xml, encoding='unicode')
                source_domain.updateDeviceFlags(disk_xml_str, 0)

        # clone source to target, reusing the now-read-only disks
        cmd = [
            'virt-clone',
            '--preserve-data',
            '--auto-clone',
            '--original',
            source,
            '--name',
            target,
        ]
        for _, disk_device, _ in cow_disks:
            cmd += ['--skip-copy', disk_device]
        subprocess.run(cmd, check=True)

        target_domain = domain(conn, target)
        try:
            for disk_file, disk_device, disk_xml in cow_disks:
                # make linked copy-on-write clone of the disk image file
                new_file = disk_file.parent / f'{target}-{disk_device}.qcow2'
                cmd = (
                    'qemu-img',
                    'create',
                    '-q',
                    '-f',
                    'qcow2',
                    '-F',
                    'qcow2',
                    '-o',
                    f'backing_file={disk_file}',
                    new_file,
                )
                subprocess.run(cmd, check=True)

                # ensure the disk is marked read/write in the target domain
                readonly_tags = disk_xml.findall('readonly')
                if readonly_tags:
                    for readonly_tag in readonly_tags:
                        disk_xml.remove(readonly_tag)
                    disk_xml_str = xml.tostring(disk_xml, encoding='unicode')
                    target_domain.updateDeviceFlags(disk_xml_str, 0)

                # set the new disk as the source file in the target domain
                # set the source file as the backing store, and append
                # source's backing store to the chain
                disk_source = disk_xml.find('source')
                source_file = disk_source.get('file')

                disk_source.set('file', str(new_file))
                backing_store = xml.Element('backingStore', {'type': 'file'})
                backing_store.append(xml.Element('format', {'type': 'qcow2'}))
                backing_store.append(xml.Element('source', {'file': source_file}))
                if source_chain := disk_xml.find('backingStore'):
                    backing_store.append(copy.copy(source_chain))
                    disk_xml.remove(source_chain)
                disk_xml.append(backing_store)

                disk_xml_str = xml.tostring(disk_xml, encoding='unicode')
                target_domain.updateDeviceFlags(disk_xml_str, 0)

        except:
            target_domain.undefine()
            raise
