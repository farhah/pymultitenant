from multitenant.users import UserDescriptor, prepare_user


class AuthenticatedUser(UserDescriptor):

    def __init__(self, response):
        attrs = prepare_user(response)
        super(AuthenticatedUser, self).__init__(attrs)

    @property
    def whoami(self):
        return self.dn

    @property
    def is_authenticated(self):
        return True

    @property
    def is_root(self):
        for item in self.groups:
            if 'root' == item.name:
                return True
        return False

    def has_group(self, group_name):
        for item in self.groups:
            if group_name == item.name:
                return True
        return False


class Authenticated(object):

    def __init__(self):
        self.__user = None

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, response):
        self.__user = AuthenticatedUser(response)


authenticated = Authenticated()
