from multitenant.utils import get_app_uuid
from multitenant.request import RequestedUser


def authenticate(func):
    def wrapper(*args, **kwargs):
        with RequestedUser() as request:
            if not request.user.dn:
                raise Exception('User is not authenticated.')
        return func(*args, **kwargs)
    return wrapper


def authorize(group):
    def wrapper(func):
        def wrapped_func(*args, **kwargs):
            with RequestedUser() as request:
                print('3 --> {}'.format(request.user))
                if not request.user:
                    raise Exception('User is not authenticated.')
                if isinstance(group, list):
                    for x in group:
                        if request.user.has_group(x):
                            return func(*args, **kwargs)
                    raise Exception('User is not authorize.')
                if not request.user.has_group(group):
                    raise Exception('User is not authorize.')
                return func(*args, **kwargs)
        return wrapped_func
    return wrapper


def within_app_dn(func):
    def wrapped_func(*args, **kwargs):
        app_dn = args[1]
        app_dn2 = args[2]
        uuid = get_app_uuid(app_dn)
        uuid2 = get_app_uuid(app_dn2)

        if uuid != uuid2:
            raise Exception('{} is not within {}'.format(app_dn, app_dn2))
        return func(*args, **kwargs)
    return wrapped_func
