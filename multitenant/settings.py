from __future__ import unicode_literals


LDAP_SETTINGS = {
    'LDAP_SERVER': 'ldap.ldapserver.io',
    'PORT': 389,
    'TLS': True,
    'LOCAL_PRIVATE_KEY_FILE': '/Users/farhah/Documents/vagrant_ldapserver/certs/ldap_server.key',
    'LOCAL_CERTIFICATE_KEY_FILE': '/Users/farhah/Documents/vagrant_ldapserver/certs/ldap_server.pem',
    'CA_CERTS_FILE': '/Users/farhah/Documents/vagrant_ldapserver/certs/ca_server.pem',
    'BASE_DC': 'dc=ldapserver,dc=io',
    'ORGANIZATION': 'ou=multitenant,dc=ldapserver,dc=io',
    'CONTAINER': 'ou=container,ou=multitenant,dc=ldapserver,dc=io',
    'ADMINISTRATOR': 'cn=admin,dc=ldapserver,dc=io',
    'PASSWORD': 'admin123',
    'TENANT_GROUPS': ['root', 'superuser', 'admin', 'supervisor', 'user']
}

OBJCLASS = [
    'top',
    'organizationalUnit',
    'groupOfNames',
    'multitenantRootUserDescriptor',
    'multitenantUserDescriptor',
    'multitenantApplicationDescriptor'
]


class MultitenantSettings(object):

    def __init__(self, user_ldap_settings=None, user_ldap_objclass=None):
        self.ldap_settings = user_ldap_settings or LDAP_SETTINGS
        if user_ldap_objclass:
            temp = list(user_ldap_objclass)
            temp = temp + OBJCLASS
            objclass = temp
        else:
            objclass = OBJCLASS

        objcls = dict(zip(objclass, objclass))
        LDAP_SETTINGS.update(objcls)

    def __getattr__(self, attr):
        if attr not in LDAP_SETTINGS:
            raise AttributeError("Invalid ldap settings: {}".format(attr))

        try:
            # Check if present in user settings
            val = self.ldap_settings[attr]
        except KeyError:
            val = LDAP_SETTINGS[attr]

        # Cache the result
        setattr(self, attr, val)
        return val


multitenant_settings = MultitenantSettings(None, None)
#
# print(multitenant_settings)
#
# print(dir(multitenant_settings))
# print(multitenant_settings.organizationalUnit)
