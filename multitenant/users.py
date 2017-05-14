from multitenant.utils import get_app_dn


def prepare_user(attrs):
    if isinstance(attrs, list):
        attrs = attrs[0]

    dn = attrs['dn']
    groups = attrs['groups']
    attrs['attributes']['dn'] = dn
    attrs['attributes']['groups'] = groups
    return attrs['attributes']


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
        self.__app_dn = get_app_dn(self.dn)
        return self.__app_dn

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
    def iduser(self):
        return self.__attrs['iduser']

    @property
    def uuid(self):
        return self.__attrs['uuid']

    @property
    def groups(self):
        return self.__attrs['groups']





