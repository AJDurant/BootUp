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
    Field('ldesc', 'text', required=True, label='Long Description', comment='What are your project goals?'),
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

# Project Virtual Fields
# Get the pledges for this project
db.project.pledges = Field.Virtual(
    'pledges',
    lambda row: db(db.pledge.projectid==row.project.id).select())
# Get the rewards for this project
db.project.rewards = Field.Virtual(
    'rewards',
    lambda row: db(db.reward.projectid==row.project.id).select())
# Calculate the total pledged
db.project.total = Field.Virtual(
    'total',
    lambda row: sum(pledge.amount for pledge in db(db.pledge.projectid==row.project.id).select()))
db.project.percent = Field.Method(lambda row: row.project.total*100/row.project.goal)

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

# Reward Virtual Fields
# Calculate backers for each reward level
db.reward.backers = Field.Virtual(
    'backers',
    lambda row: sum(pledge.amount >= row.reward.amount for pledge in db(db.pledge.projectid==row.reward.projectid).select()))


# Lookup table for project pledges
db.define_table(
    'pledge',
    Field('projectid', 'reference project', writable=False, readable=False, required=True),
    Field('userid', 'reference auth_user', writable=False, readable=False, required=True),
    Field('amount', 'integer', required=True, comment='Amount to pledge to the Bootable in whole £s')
)

# Pledge Virtual Fields
# Get user data for pledger
db.pledge.pledger = Field.Virtual(
    'pledger',
    lambda row: db.auth_user(row.pledge.userid))

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
    Field('post1', length=4, required=True, label='Post Code (1)', comment='The outward code, eg. YO10'),
    Field('post2', length=3, required=True, label='Post Code (2)', comment='The inward code, eg. 5DD'),
    format='%(street)s'
)
# TODO constraints

# DB Table for User Credit Cards
db.define_table(
    'cc',
    Field('userid', 'reference auth_user', writable=False, readable=False, required=True),
    Field('address', 'reference address', required=True, comment='Billing address associated with the card'),
    Field('ccnum', length=12, required=True, label='Card Number', comment='Full 12 digit card number. Note this is not stored securely.'),
    Field('expires', 'date', required=True, label='Expiry Date', comment='Date format is YYYY-MM-DD'),
    Field('pic', 'integer', required=True, label='CVC', comment='3 digit security code on back of card. Note this should not be stored by any reputable organisation, they will get fined for doing so.')
)
# TODO constraints

