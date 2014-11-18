"""
This model initialises the database tables for app


"""



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
    Field('title', required=True, label='Bootable Title'),
    Field('category', 'reference category', required=True),
    Field('status', 'reference status', writable=False, readable=False, required=True),
    Field('goal', 'integer', required=True, label='Funding Goal', comment='What do you aim to raise? (in GBP £)'),
    Field('img', 'upload', autodelete=True, uploadseparate=True, label='Image', comment='Give your Bootable an image. Max Size: 1024x768 (jpg, png or gif) recommended: 4:3 ratio'),
    Field('sdesc', 'string', length=120, required=True, label='Short Description', comment='Describe your Bootable in 120 characters or less.'),
    Field('ldesc', 'text', required=True, label='Long Description'),
    Field('story', 'text', required=True, label='Story', comment='Why do you want this project funded?'),
    Field('manager', 'reference auth_user', writable=False, readable=False, required=True),
    format='%(title)s'
)

# Project data constraints
db.project.title.requires = IS_NOT_EMPTY()
db.project.category.requires = IS_IN_DB(db, db.category.id, '%(name)s', error_message='You must select a category')
db.project.status.requires = IS_IN_DB(db, db.status.id, '%(name)s')
db.project.goal.requires = IS_NOT_EMPTY()
db.project.img.requires = IS_IMAGE(extensions=('png', 'jpg', 'jpeg', 'gif'), maxsize=(1024, 768))
db.project.sdesc.requires = IS_NOT_EMPTY()
db.project.ldesc.requires = IS_NOT_EMPTY()
db.project.story.requires = IS_NOT_EMPTY()
db.project.manager.requires = IS_IN_DB(db, db.auth_user.id, '%(username)s')

# Lookup table for project rewards
db.define_table(
    'reward',
    Field('projectid', 'reference project', writable=False, readable=False, required=True),
    Field('amount', 'integer', required=True, comment='Minimum pledge to receive this reward in whole £s'),
    Field('reward', required=True,
        widget=SQLFORM.widgets.text.widget,
        comment='Description of the reward given to those who pledge over the required amount')
)

# Reward data constraints
db.reward.projectid.requires = IS_IN_DB(db, db.project.id, '%(title)s')
db.reward.amount.requires = IS_NOT_EMPTY()
db.reward.reward.requires = IS_NOT_EMPTY()

# Lookup table for project pledges
db.define_table(
    'pledge',
    Field('projectid', 'reference project', writable=False, readable=False, required=True),
    Field('userid', 'reference auth_user', required=True),
    Field('amount', 'integer', required=True)
)

# Pledge data constraints
db.pledge.projectid.requires = IS_IN_DB(db, db.project.id, '%(title)s')
db.pledge.userid.requires = IS_IN_DB(db, db.auth_user.id, '%(username)s')
db.pledge.amount.requires = IS_NOT_EMPTY()

# DB Table for User Addresses
db.define_table(
    'address',
    Field('userid', 'reference auth_user', writable=False, readable=False, required=True),
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
    Field('userid', 'reference auth_user', writable=False, readable=False, required=True),
    Field('address', 'reference address', required=True),
    Field('ccnum', required=True),
    Field('expires', 'date', required=True),
    Field('pic', 'integer', required=True)
)

