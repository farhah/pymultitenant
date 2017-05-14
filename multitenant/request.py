from multitenant.authenticatedUser import authenticated
from multitenant.baseOperation import BaseOperation


class RequestUser(BaseOperation):

    def __enter__(self):
        self.__user = None
        return self.user

    @property
    def user(self):
        if not self.__user:
            return self.__set_user()
        return self.__user

    def __set_user(self):
        raw_data = self.get_user(authenticated.user.iduser, authenticated.user.app_dn)[0]
        raw_data['groups'] = self.get_user_groups(authenticated.user.whoami, authenticated.user.app_dn)
        authenticated.user = raw_data
        self.__user = authenticated
        return self.__user

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__user = None
