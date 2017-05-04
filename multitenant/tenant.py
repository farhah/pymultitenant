from multitenant.auth import auth
from multitenant.settings import MultitenantSettings as settings
from multitenant.ldap3 import MODIFY_REPLACE, MODIFY_ADD, MODIFY_DELETE


class Tenant(object):

    def __init__(self, user, password):
        self.user, self.ldap = auth(user, password)
        self.password = password

    def list_dn(self, stuff):
        list_stuff = list()
        for x in stuff['response']:
            list_stuff.append(x['dn'])

        return list_stuff

    def list_attributes(self, stuff):
        list_stuff = list()
        for x in stuff['response']:
            list_stuff.append(x['attributes'])

        return list_stuff

    def list_applications(self):
        apps = self.ldap.search(self.user, '(objectClass=' + settings.multitenantApplicationDescriptor + ')',
                                attributes=['*'], user=self.user, password=self.password)
        list_app = self.list_attributes(apps)
        return list_app

    def list_groups(self, app_dn):
        groups = self.ldap.search(app_dn, '(objectClass=' + settings.groupOfNames + ')',
                                  user=self.user, password=self.password)
        list_group = self.list_dn(groups)
        return list_group

    def list_users(self, app_dn):
        users = self.ldap.search(app_dn, '(objectClass=' + settings.multitenantUserDescriptor + ')',
                                 attributes=['*'], user=self.user, password=self.password)
        list_user = self.list_attributes(users)
        return list_user

    def list_group_members(self, app_dn):
        group_members = self.ldap.search(app_dn, '(objectClass=' + settings.groupOfNames + ')', attributes=['member'],
                                         user=self.user, password=self.password)

        gr_dict = dict()
        for gr in group_members['response']:
            gr_dict[gr['dn']] = gr['attributes']['member']

        return gr_dict

    def is_app_enable(self, app_dn):
        app = self.ldap.search(app_dn, '(objectClass=' + settings.multitenantApplicationDescriptor + ')',
                               attributes=['isEnable'], user=self.user, password=self.password)
        status = app['response'][0]['attributes']['isEnable'][0]  # the first element in list is the value
        return status

    def disable_app(self, app_dn):
        app = self.ldap.modify(app_dn, {'isEnable': [(MODIFY_REPLACE, ['FALSE'])]}, user=self.user, password=self.password)
        return app['status']

    def assign_user_to_group(self, assigned_user, user_dn, group_dn, app_dn):
        is_enable = self.is_app_enable(app_dn)
        if is_enable == 'FALSE':
            raise Exception("Can't edit disable app.")

        users = self.list_users(app_dn)
        user = [user for user in users if user['uid'] == assigned_user][0]
        if not user:
            raise Exception('User does not exist.')

        modified_user = self.ldap.modify(group_dn, {'member': [(MODIFY_ADD, [user_dn])]},
                                         user=self.user, password=self.password)

        return modified_user['status']

    def remove_user_from_group(self, assigned_user, user_dn, group_dn, app_dn):
        is_enable = self.is_app_enable(app_dn)
        if is_enable == 'FALSE':
            raise Exception("Can't edit disable app.")

        users = self.list_users(app_dn)
        user = [user for user in users if user['uid'] == assigned_user][0]
        if not user:
            raise Exception('User does not exist.')

        modified_user = self.ldap.modify(group_dn, {'member': [(MODIFY_DELETE, [user_dn])]},
                                         user=self.user, password=self.password)

        return modified_user

    def change_url_alias(self, app_uuid, rootuser, rootpassword):
        self.is_app_enable(app_uuid, rootuser, rootpassword)
        pass

    def get_url(self, app_uuid, rootuser, rootpassword):
        pass

    def get_url_alias(self, app_uuid, rootuser, rootpassword):
        pass
