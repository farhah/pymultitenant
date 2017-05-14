from multitenant.settings import multitenant_settings as settings
from multitenant.connect import ldap
from multitenant import validation
from multitenant.groups import list_groups


class Operation(object):

    def search(self, *args, **kwargs):
        data = ldap.search(*args, **kwargs)
        if data['result']['description'] != 'success':
            msg = data['result']['message']
            desc = data['result']['description']
            raise Exception(validation.bad_request(msg, desc))
        return data

    def modify(self, *args, **kwargs):
        data = ldap.modify(*args, **kwargs)
        if data['result']['description'] != 'success':
            msg = data['result']['message']
            desc = data['result']['description']
            raise Exception(validation.bad_request(msg, desc))
        return data

    def modify_dn(self, *args, **kwargs):
        data = ldap.modify_dn(*args, **kwargs)
        if data['result']['description'] != 'success':
            msg = data['result']['message']
            desc = data['result']['description']
            raise Exception(validation.bad_request(msg, desc))
        return data['response']

    def delete(self, *args, **kwargs):
        data = ldap.delete(*args, **kwargs)
        if data['result']['description'] != 'success':
            msg = data['result']['message']
            desc = data['result']['description']
            raise Exception(validation.bad_request(msg, desc))
        return data

    def add(self, *args, **kwargs):
        data = ldap.add(*args, **kwargs)
        if data['result']['description'] != 'success':
            msg = data['result']['message']
            desc = data['result']['description']
            raise Exception(validation.bad_request(msg, desc))
        return data


class BaseOperation(Operation):

    """ return raw data """

    def get_user(self, iduser, app_dn):
        search_filter = '(&(objectClass=' + settings.multitenantUserDescriptor + ')(iduser=' + iduser + '))'
        data = self.search(app_dn, search_filter,
                           attributes=['*'])
        return data['response']

    def get_user_groups(self, whoami, app_dn):
        search_filter = '(&(objectClass=' + settings.groupOfNames + ')(member=' + whoami + '))'
        data = self.search(app_dn, search_filter)
        groups = list_groups(data['response'])
        return groups
