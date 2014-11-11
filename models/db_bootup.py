
# DB Table for BootUp Projects
db.define_table(
    'project',
    Field('title'),
    Field('category', 'reference category'),
    Field('status', 'reference status'),
    Field('goal', 'integer'),
    Field('img', 'upload', autodelete=True, uploadseparate=True),
    Field('sdesc', 'string', length=120, required=True),
    Field('ldesc', 'text'),
    Field('story', 'text'),
    Field('manager', 'reference user'),
    format='%(title)s'
)

# Lookup table for categories
db.define_table(
    'category',
    Field('name'),
    format='%(name)s'
)

# Lookup table for project status
db.define_table(
    'status',
    Field('name'),
    format='%(name)s'
)

# Lookup table for project rewards
db.define_table(
    'reward',
    Field('projectid', 'reference project'),
    Field('amount', 'integer'),
    Field('reward')
)

# Lookup table for project pledges
db.define_table(
    'pledge',
    Field('projectid', 'reference project'),
    Field('uname', 'reference user'),
    Field('amount', 'integer')
)


# DB Table for BootUp Users
db.define_table(
    'user',
    Field('uname'),
    Field('realname'),
    Field('birthdate', 'date'),
    format='%(realname)s (%(uname)s)'
)

# DB Table for User Addresses
db.define_table(
    'address',
    Field('uname', 'reference user'),
    Field('street'),
    Field('city'),
    Field('country'),
    Field('post1'),
    Field('post2')
)

# DB Table for User Credit Cards
db.define_table(
    'cc',
    Field('uname', 'reference user'),
    Field('address', 'reference address'),
    Field('number'),
    Field('expires', 'date'),
    Field('pic', 'integer')
)

