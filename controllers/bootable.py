"""
This is the bootable controller
 - project displays project information
 - create is used to create new projects
 - edit is used to update projects and add reward goals
 - manager is used to view a users bootables and access edit for them


"""

def view():
    """
    Bootable Pages and Pledging

    For each project that is Open for Pledges, funders will be able visit a page where they
    can get information about a Bootable. This page should show the funding goal and the
    total pledged progress toward that goal and the pledge/reward options for the project.
    The page should also show the usernames of those who have contributed, what they
    have contributed and what their expected rewards will be.
    Users can choose to pledge money to a Bootable from a pre-defined set of pledge values
    (referred to by users as “a Booting”) in exchange for a pre-defined set of rewards.
    When users pledge money to the total pledged, their name and pledge level is added to
    the list of pledgers. Further, when users visit pages to which they have already pledged,
    that page should indicate
    """

    project = db.project(request.args(0,cast=int)) or redirect(URL('default', 'index'))

    # Make 'not available' projects unviewable
    if project.status == 1:
        redirect(URL('default', 'index'))

    # Set page title
    response.title = project.title
    response.subtitle = project.sdesc

    # Get the referenced lookup infomation
    project.category = db.category(project.category)
    project.status = db.status(project.status)
    manager = db.auth_user(project.manager)

    # Get project rewards as a python list of dicts
    project.rewards = db(db.reward.projectid==project.id).select().as_list()

    # Get project pledges and calcumate progress
    project.pledges = db(db.pledge.projectid==project.id).select().as_list()
    project.total = sum(pledge['amount'] for pledge in project.pledges)
    project.percent = (project.total * 100) / project.goal

    # Calculate backers for each reward level
    for i,reward in enumerate(project.rewards):
        project.rewards[i]['backers'] = sum(pledge['amount'] >= reward['amount'] for pledge in project.pledges)

    for i,pledge in enumerate(project.pledges):
        project.pledges[i]['username'] = db(db.auth_user.id==pledge['userid']).select().first().username



    return locals()

@auth.requires_login()
def pledge():
    """
    Bootable Pledging

    Users can choose to pledge money to a Bootable from a pre-defined set of pledge values
    (referred to by users as “a Booting”) in exchange for a pre-defined set of rewards.
    When users pledge money to the total pledged, their name and pledge level is added to
    the list of pledgers. Further, when users visit pages to which they have already pledged,
    that page should indicate
    """

    # Get project or redirect
    project = db.project(request.args(0,cast=int)) or redirect(URL('default', 'index'))

    pledgeform = SQLFORM(db.pledge, formstyle='bootstrap3_inline')

    pledgeform.vars.projectid = project.id
    pledgeform.vars.userid = auth.user_id

    if pledgeform.process().accepted:
        session.flash = 'Bootable Pledged'
        redirect(URL('bootable', 'view', args=project.id))
    elif pledgeform.errors:
        response.flash = 'Error with form'
    else:
        pass

    response.title = 'Give A Booting'
    response.subtitle = project.title

    return locals()

@auth.requires_login()
def create():
    """
    Creating Bootables

    Users of BootUp will have the ability to create projects that consist of all of the information
    mentioned above in the section about BootUp Projects. When projects are created,
    they will be inactive and have the status Not Available. After creating a Bootable, the BM
    should be presented with the Bootable Editor.
    """
    # Set page title
    response.title = 'Create a Bootable'

    # Setup form, using bootstrap style - not tables!
    form = SQLFORM(db.project, formstyle='bootstrap3_inline')

    # Set project status to 'Not Available'
    form.vars.status = 1
    # Set manager to the logged in user
    form.vars.manager = auth.user_id

    if form.process().accepted:
        session.flash = 'Bootable Created'
        redirect(URL('bootable', 'edit', args=project.id))
    elif form.errors:
        response.flash = 'Error with form'
    else:
        pass

    return locals()


@auth.requires_login()
def edit():
    """
    Bootable Editor

    BMs can change all of the information contained within their project provided the project
    has not been moved to be Open for Pledges. If the project is Open for Pledges then the
    information about the project can no longer be changed.
    """
    # Get project or redirect
    project = db.project(request.args(0,cast=int)) or redirect(URL('default', 'index'))

    # Stop non-managers from editing the Bootable
    if project.manager != auth.user_id:
        redirect(URL('default', 'index'))

    # Setup forms, using bootstrap style - not tables!
    editform = SQLFORM(db.project, project, formstyle='bootstrap3_inline')
    rewardform = SQLFORM(db.reward, formstyle='bootstrap3_inline')

    rewardform.vars.projectid = project.id

    if editform.process().accepted:
        session.flash = 'Bootable Updated'
        redirect(URL('bootable', 'view', args=project.id))
    elif editform.errors:
        response.flash = 'Error with form'
    else:
        pass

    if rewardform.process().accepted:
        response.flash = 'Reward Added'
    elif rewardform.errors:
        response.flash = 'Error with form'
    else:
        pass

    # Set page title
    response.title = 'Edit Bootable: ' + project.title

    # Get rewards - this happens after form processing, so that latest reward is added
    rewards = db(db.reward.projectid==project.id).select()

    return dict(rewards=rewards, editform=editform, rewardform=rewardform)

@auth.requires_login()
def manager():
    """
    Bootable Manager Dashboard

    BMs will manage their projects from a Bootable Manager Dashboard. The Dashboard
    will give BMs an overview of all of their projects including: the current status of all
    projects, the amount pledged towards the final goal (if applicable) and the funding goal.
    The Dashboard should allow users to open a project to pledges or close it. BMs should
    be able to visit any of their Bootables from this page. BMs should be able to delete any of
    their Bootables from this page, but only if they are not Open for Pledges.
    """

    return dict()
