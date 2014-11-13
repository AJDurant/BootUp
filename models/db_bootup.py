
# DB Table for BootUp Users in db.py for auth


# Lookup table for categories
db.define_table(
    'category',
    Field('name', required=True),
    format='%(name)s'
)

# Lookup table for project status
db.define_table(
    'status',
    Field('name', required=True),
    format='%(name)s'
)

# DB Table for BootUp Projects
db.define_table(
    'project',
    Field('title', required=True),
    Field('category', 'reference category', required=True),
    Field('status', 'reference status', required=True),
    Field('goal', 'integer', required=True),
    Field('img', 'upload', autodelete=True, uploadseparate=True),
    Field('sdesc', 'string', length=120, required=True),
    Field('ldesc', 'text', required=True),
    Field('story', 'text', required=True),
    Field('manager', 'reference auth_user', writable=False, readable=False, required=True),
    format='%(title)s'
)

db.project.manager.requires = IS_IN_DB(db, db.auth_user.id, '%(uname)s')

# Lookup table for project rewards
db.define_table(
    'reward',
    Field('projectid', 'reference project', writable=False, readable=False, required=True),
    Field('amount', 'integer', required=True),
    Field('reward', required=True)
)

# Lookup table for project pledges
db.define_table(
    'pledge',
    Field('projectid', 'reference project', writable=False, readable=False, required=True),
    Field('username', 'reference auth_user', required=True),
    Field('amount', 'integer', required=True)
)

# DB Table for User Addresses
db.define_table(
    'address',
    Field('username', 'reference auth_user', writable=False, readable=False, required=True),
    Field('street', required=True),
    Field('city', required=True),
    Field('country', required=True),
    Field('post1', required=True),
    Field('post2', required=True),
    format='%(street)s'
)

# DB Table for User Credit Cards
db.define_table(
    'cc',
    Field('username', 'reference auth_user', writable=False, readable=False, required=True),
    Field('address', 'reference address', required=True),
    Field('ccnum', required=True),
    Field('expires', 'date', required=True),
    Field('pic', 'integer', required=True)
)

