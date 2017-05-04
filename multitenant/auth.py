from multitenant.connect import ldap
from multitenant.users import objectify_user
from multitenant.settings import multitenant_settings as settings
from multitenant.validation import bad_request


def auth(user, password):
    auth_user, msg = ldap.auth(user=user, password=password)
    if not auth_user:
        bad = bad_request(msg=msg)
        return bad
    return auth_user



# test = UserOperation(ldap)
# test.get_all_users('applicationUUID=074eb119-b954-5c6b-94eb-0ad3898e6ff0,email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io',
#                    requested_user=user)
#
#
# l = test.get_user('uid=mok,ou=users,applicationUUID=074eb119-b954-5c6b-94eb-0ad3898e6ff0,email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io',
#                   'applicationUUID=074eb119-b954-5c6b-94eb-0ad3898e6ff0,email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io',
#                   requested_user=user)
# print(l)


#
# test.delete_user('uid=farhah_email_empID,ou=users,applicationUUID=074eb119-b954-5c6b-94eb-0ad3898e6ff0,email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io',
#                  'applicationUUID=074eb119-b954-5c6b-94eb-0ad3898e6ff0,email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io',
#                  requested_user=user)


# groups = ldap.search('applicationUUID=074eb119-b954-5c6b-94eb-0ad3898e6ff0,email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io',
#                      '(&(objectClass=groupOfNames)(member=farhah_email_empID))',
#                      requested_user=user)
# #
# print(groups)

# print(a.whoami)
# print(a.is_authenticated)
# #
# b = auth('cn=admin,dc=ldapserver,dc=io', 'admin123')
# print(b.whoami)
# print(b.is_authenticated)
#
# print(a.whoami)

# ldap = ConnectLDAP()
# a = ldap.search('uid=farhah_email_empID,ou=users,applicationUUID=074eb119-b954-5c6b-94eb-0ad3898e6ff0,email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io',
#                 '(&(objectClass=multitenantUserDescriptor)(uid=farhah_email_empID))',
#                 attributes=['*'],
#                 request_user=user)
# print('------------------')
# print(a)
#
# a = ldap.search('email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io', '(objectClass=multitenantApplicationDescriptor)',
#                 attributes=['*'])
# print(a)

#
# a = ldap.search('email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io', '(objectClass=multitenantApplicationDescriptor)',
#                 attributes=['*'], request_user=user)
# print(a)
#
# groups = ldap.search('applicationUUID=074eb119-b954-5c6b-94eb-0ad3898e6ff0,email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io',
#                      '(&(objectClass=groupOfNames)(member=email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io))',
#                      attributes=['*'], request_user=user)
# #
# print(groups)

# a = ldap.search('email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io', '(&(objectClass=multitenantUserDescriptor)(uid=farhah_email_empID))',
                # attributes=['*'], request_user=user)

# a = ldap.search('email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io', '(objectClass=multitenantApplicationDescriptor)',
#                 attributes=['*'])
# print(a)
