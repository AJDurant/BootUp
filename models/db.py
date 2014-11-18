"""
This model initialises the database and constructs the auth object and tables


"""

from gluon.custom_import import track_changes; track_changes(True)

from datetime import date

# Setup db object
db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

# setup auth module
# this is a custom module due to overriding Auth.navbar()
# the bug in Auth.navbar() has been reported
from myAuth import myAuth
auth = myAuth(db)


# Define custom user table
db.define_table(
    auth.settings.table_user_name,
    Field('username', length=128, unique=True),
    Field('realname', length=128, default='', label='Name'),
    Field('birthdate', 'date', required=True, comment='format: YYYY-MM-DD'),
    Field('email', length=128, default='', unique=True),                                    # required
    Field('password', 'password', length=512, readable=False, label='Password'),            # required
    Field('registration_key', length=512, writable=False, readable=False, default=''),      # required
    Field('reset_password_key', length=512, writable=False, readable=False, default=''),    # required
    Field('registration_id', length=512, writable=False, readable=False, default=''),       # required
    format='%(realname)s (%(username)s)')



## do not forget validators
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.username.requires = [IS_NOT_EMPTY(error_message=auth.messages.is_empty), IS_NOT_IN_DB(db, custom_auth_table.username)]
custom_auth_table.realname.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [IS_STRONG(), CRYPT()]
custom_auth_table.email.requires = [
    IS_EMAIL(error_message=auth.messages.invalid_email),
    IS_NOT_IN_DB(db, custom_auth_table.email)]

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)


## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# set formstyle to nice bootstrap
auth.settings.formstyle = 'bootstrap3_inline'
