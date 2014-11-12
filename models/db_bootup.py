
# DB Table for BootUp Users
db.define_table(
    'person',
    Field('uname', unique=True, required=True),
    Field('realname', required=True),
    Field('birthdate', 'date', required=True),
    format='%(realname)s (%(uname)s)'
)

db.person.uname.requires = IS_NOT_IN_DB(db, db.person.uname)

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
    Field('manager', 'reference person', required=True),
    format='%(title)s'
)

db.project.manager.requires = IS_IN_DB(db, db.person.id, '%(uname)s')

# Lookup table for project rewards
db.define_table(
    'reward',
    Field('projectid', 'reference project', required=True),
    Field('amount', 'integer', required=True),
    Field('reward', required=True)
)

# Lookup table for project pledges
db.define_table(
    'pledge',
    Field('projectid', 'reference project', required=True),
    Field('uname', 'reference person', required=True),
    Field('amount', 'integer', required=True)
)

# DB Table for User Addresses
db.define_table(
    'address',
    Field('uname', 'reference person', required=True),
    Field('street', required=True),
    Field('city', required=True),
    Field('country', required=True),
    Field('post1', required=True),
    Field('post2', required=True)
)

# DB Table for User Credit Cards
db.define_table(
    'cc',
    Field('uname', 'reference person', required=True),
    Field('address', 'reference address', required=True),
    Field('ccnum', required=True),
    Field('expires', 'date', required=True),
    Field('pic', 'integer', required=True)
)

