from multitenant.users import UserDescriptor, prepare_user
from multitenant.settings import multitenant_settings as settings
from multitenant.groups import list_groups


class AuthenticatedUser(UserDescriptor):

    def __init__(self, response):
        attrs = prepare_user(response)
        super(AuthenticatedUser, self).__init__(attrs)
        # server_conn, bind = server()
        # with Connection(server_conn, settings.ADMINISTRATOR, settings.PASSWORD, auto_bind=bind, client_strategy=REUSABLE) as conn:
        #     if self.is_owner:
        #         email = self.whoami.split(',')[0].partition('email=')[-1]
        #         search_filter = '(&(objectClass=' + settings.multitenantRootUserDescriptor + ')(email=' + email + '))'
        #         pool_counter = conn.search(self.whoami, search_filter, attributes=['*'])
        #         response, result = conn.get_response(pool_counter)
        #         user = list_users(response)
        #         self.attributes = user[0]  # can only have 1 user

    @property
    def whoami(self):
        return self.dn

    @property
    def is_authenticated(self):
        return True

    @property
    def is_owner(self):
        if self.whoami.startswith('uid'):
            return False
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
