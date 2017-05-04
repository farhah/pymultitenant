from multitenant.settings import multitenant_settings as settings
from multitenant.connect import ldap
import multitenant.validation
from multitenant.utils import get_app_dn, is_within_app_dn


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
        print(data)
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

    def get_user(self, user_dn):
        user = user_dn.split(',')[0].partition('uid=')[-1]
        app_dn = get_app_dn(user_dn)
        is_within_app_dn(user_dn, app_dn)
        search_filter = '(&(objectClass=' + settings.multitenantUserDescriptor + ')(uid=' + user + '))'
        data = self.search(app_dn, search_filter,
                           attributes=['*'])
        return data

    def get_user_groups(self, user_dn):
        search_filter_group = '(&(objectClass=groupOfNames)(member=' + user_dn + '))'
        app_dn = get_app_dn(user_dn)
        is_within_app_dn(user_dn, app_dn)
        data = ldap.search(app_dn, search_filter_group, attributes=['*'])
        return data
