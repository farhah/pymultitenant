import re


def get_domain(base_dc):
    compiled = re.compile(r'dc=(\w+)')
    match = compiled.findall(base_dc)
    domain = '.'.join(match)
    return domain


def get_app_dn(dn):
    searched = re.search(r'applicationUUID=([^,]+),.*', dn)
    app_dn = searched.group()
    return app_dn


def get_app_uuid(dn):
    searched = re.search(r'applicationUUID=([^,]+),.*', dn)
    app_uuid = searched.group(1)
    return app_uuid


def get_uid(dn):
    searched = re.search(r'uid=([^,]+),.*', dn)
    uid = searched.group(1)
    return uid


def is_within_app_dn(dn1, dn2):
    uuid = get_app_uuid(dn1)
    uuid2 = get_app_uuid(dn2)

    if uuid != uuid2:
        raise Exception('{} is not within {}'.format(dn1, dn2))
    return True
