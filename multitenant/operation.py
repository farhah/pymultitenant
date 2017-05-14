from multitenant.baseOperation import BaseOperation
from multitenant.decorators import authenticate, authorize
from multitenant.settings import multitenant_settings as settings
from multitenant.authenticatedUser import authenticated
from ldap3 import MODIFY_REPLACE
from multitenant.groups import objectify_group
from multitenant.utils import get_app_dn
from multitenant.users import prepare_user, UserDescriptor


class UserOperation(BaseOperation):

    def objectify_user(self, attrs):
        """
        attrs of response either dict or list but with only len 1
    
        attrs = [{'raw_attrs': {}, 'attrs': {}, 'type': 'something'},
                                     {'raw_attrs': {}, 'attrs': {}, 'type': 'something'}, ..]
        :param attrs:
        :return:
        """
        whoami = attrs['dn']
        app_dn = get_app_dn(whoami)
        groups = self.get_user_groups(whoami, app_dn)
        attrs['groups'] = groups

        attributes = prepare_user(attrs)

        user = UserDescriptor(attributes)
        return user

    def list_users(self, attrs_dict):
        users = list()
        for attrs in attrs_dict:
            user = self.objectify_user(attrs)
            users.append(user)

        return users

    @authorize(['admin', 'superuser', 'root'])
    def get_all_users(self, search_base):
        search_filter = '(objectClass=' + settings.multitenantUserDescriptor + ')'
        data = self.search(search_base, search_filter,
                           attributes=['*'])
        users = self.list_users(data['response'])
        return users

    @authorize(['admin', 'superuser', 'root'])
    def get_one_user(self, user_dn):
        data = self.get_user(user_dn)
        user = self.objectify_user(data['response'])
        return user

    @authorize(['admin', 'superuser', 'root'])
    def delete_user(self, user_obj):
        groups = user_obj.groups

        if user_obj.dn == authenticated.user.dn:
            raise Exception('{} cannot delete itself.'.format(user_obj.dn))

        for user_to_del in groups:
            for req_user_group in authenticated.user.groups:
                if req_user_group.name == 'admin' and user_to_del.name in ['admin', 'superuser', 'root']:
                    raise Exception('Admin cannot delete other admins, superusers and root')
                elif req_user_group.name == 'superuser' and user_to_del.name in ['root']:
                    raise Exception('Superuser cannot delete root')
                elif req_user_group.name == 'root' and user_to_del.name == 'root':
                    raise Exception('Root cannot delete itself.')

        data = self.delete(user_obj.dn)
        if data['result']['description'] == 'success':
            return True

        return False

    @authorize(['admin', 'superuser', 'root'])
    def create_user(self):
        pass

    @authorize(['admin', 'superuser', 'root'])
    def modify_user_group(self, user_obj):
        pass

    @authorize(['admin', 'superuser', 'root'])
    def modify_user(self, user_obj, changes=None):
        """
        if self must not be user_obj. At front-end must not allow edit self.
        :param user_obj: get it from the method get_user
        :param changes: dict of {field: val, field2: val}
        :return: True
        """
        if user_obj.dn == authenticated.user.dn:
            raise Exception('To modify yourself please use edit profile.')

        groups = user_obj.groups

        for group in groups:
            for req_user_group in authenticated.user.groups:
                if req_user_group.name == 'admin' and group.name in ['admin', 'superuser', 'root']:
                    raise Exception('Admin cannot modify attributes of other admins, superusers and root')
                elif req_user_group.name == 'superuser' and group.name in ['root']:
                    raise Exception('Superuser cannot modify attributes of root')

        changes_ = dict()
        for key, val in changes.items():
            changes_[key] = [(MODIFY_REPLACE, [val])]

        data = self.modify(user_obj.dn, changes_)

        if data['result']['description'] == 'success':
            return True

        return False


class GroupOperation(BaseOperation):

    def delete_group(self):
        pass

    def create_group(self):
        pass

    def get_user_group(self, user_dn, app_dn):
        search_filter_group = '(&(objectClass=groupOfNames)(member=' + user_dn + '))'
        data = self.search(app_dn, search_filter_group, attributes=['*'])
        groups = objectify_group(data['response'])
        return groups


class UserProfile(BaseOperation):

    @authenticate
    def edit_uid(self, new_uid):
        """
        client provided changes = { 'givenName': 'givenname-1-replaced',
                    'sn': 'sn-replaced'
                  }
        into ldap changes
        {
         'givenName': [(MODIFY_REPLACE, ['givenname-1-replaced'])],
         'sn': [(MODIFY_REPLACE, ['sn-replaced'])]
         }

        :param new_uid: just uid without long dn.
        :return:
        """

        print(authenticated.user.dn)

        # changes_ = dict()
        # for key, val in changes.items():
        # changes_['uid'] = [(MODIFY_REPLACE, [new_uid])]
        # print(changes_)

        data = self.modify_dn(authenticated.user.dn, 'uid=' + new_uid)
        return True

    def edit_password(self):
        pass

    def edit_group(self):

        """
        if self is admin/superuser/root can't downgrade group.
        But can add other groups(less power than admin/superuser/root) if available.
        :return:
        """
        pass

    def edit_email(self):
        pass
