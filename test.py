from multitenant.auth import auth
from multitenant.operation import UserOperation, UserProfile


authenticated = auth('iduser=farhah_email_empID,ou=users,applicationUUID=c2e3850d-882d-5273-80e5-6b2b5f7f622d,email=mom13@momo.com,ou=container,ou=multitenant,dc=ldapserver,dc=io', 'mypassword')
print('----------------')
print(authenticated.user.dn)
print(authenticated.user.groups)
for x in authenticated.user.groups:
    print(x.name)
    print(x.dn)

print('------11111111')
# #
# # #
# test = UserOperation()
# a = test.get_all_users('applicationUUID=074eb119-b954-5c6b-94eb-0ad3898e6ff0,email=mom13@momo.com,ou=rootuser,ou=multitenant,dc=ldapserver,dc=io')
# for x in a:
#     print(x.dn, '-----> ' + x.groups.name, '------> ' + x.groups.dn)
# #
# # # #
# z = UserProfile()
# a = z.edit_uid('nanas')
