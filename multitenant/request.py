from multitenant.authenticatedUser import authenticated
from multitenant.baseOperation import BaseOperation


class RequestedUser(BaseOperation):

    def __enter__(self):
        self.__user = None
        return self.user

    @property
    def user(self):
        if not self.__user:
            return self.__set_user()
        return self.__user

    def __set_user(self):
        user_dn = authenticated.user.dn
        print('1 --> {}'.format(authenticated.user))
        raw_data = self.get_user(user_dn)
        authenticated.user = raw_data['response']
        raw_data_group = self.get_user_groups(user_dn)
        authenticated.user.groups = raw_data_group['response']
        print('2 --> {}'.format(authenticated.user))
        self.__user = authenticated
        return self.__user

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__user = None
