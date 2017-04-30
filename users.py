from multitenant.utils import get_app_dn
from multitenant.groups import objectify_group
from multitenant.settings import multitenant_settings as settings


def get_user_group(user_dn, search_func, search_base):
    search_filter = '(&(objectClass=' + settings.groupOfNames + ')(member=' + user_dn + '))'
    data = search_func(search_base, search_filter)
    groups = objectify_group(data['response'][0])
    return groups


def prepare_user(attrs):
    if isinstance(attrs, list):
        attrs = attrs[0]

    dn = attrs['dn']
    attrs['attributes']['dn'] = dn

    return attrs['attributes']


def objectify_user(attrs, search_func):
    """
    attrs of response either dict or list but with only len 1

    attrs = [{'raw_attrs': {}, 'attrs': {}, 'type': 'something'},
                                 {'raw_attrs': {}, 'attrs': {}, 'type': 'something'}, ..]
    :param attrs:
    :param search_func: is used to search groups belonged to each users
    :return:
    """

    attributes = prepare_user(attrs)
    dn = attributes['dn']
    search_base = get_app_dn(dn)

    groups = get_user_group(dn, search_func, search_base)
    attributes['groups'] = groups

    user = UserDescriptor(attributes)
    return user


def list_users(attrs_dict, search_func):
    """
    attrs_dict = dict of response with many len
    :param search_func: is used to search groups belonged to each users
    """
    users = list()
    for attrs in attrs_dict:
        user = objectify_user(attrs, search_func)
        users.append(user)

    return users


class UserDescriptor(object):

    """
    Given a dict of User attributes, UserDescriptor will objectify them.
    """
    def __init__(self, user_attrs):
        self.__attrs = user_attrs
        self.__app_dn = None

    @property
    def dn(self):
        return self.__attrs['dn']

    @property
    def app_dn(self):
        return self.__app_dn

    @app_dn.setter
    def app_dn(self, value):
        self.__app_dn = get_app_dn(self.dn)

    @property
    def email(self):
        return self.__attrs['email']

    @property
    def is_active(self):
        value = self.__attrs['isActive']
        if value == 'FALSE':
            return False
        return True

    @property
    def uid(self):
        return self.__attrs['uid']

    @property
    def uuid(self):
        return self.__attrs['uuid']

    @property
    def groups(self):
        return self.__attrs['groups']





