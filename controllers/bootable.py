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
    if project.status.id == 1:
        redirect(URL('default', 'index'))

    # Set page title
    response.title = project.title
    response.subtitle = project.sdesc

    # Get the referenced lookup infomation
    manager = db.auth_user(project.manager)

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
        redirect(URL('bootable', 'edit', args=form.vars.id))
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
        redirect(URL('bootable', 'view', args=[project.id]))
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
    response.title = 'Edit Bootable'
    response.subtitle = project.title

    # Get rewards - this happens after form processing, so that latest reward is added
    project.rewards = db(db.reward.projectid==project.id).select()

    # Disable editing if project has been opened
    if project.status != 1:
        editform = None
        rewardform = None

    return locals()

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

    response.title = 'Bootable Manager'

    projects = db(db.project.manager == auth.user_id).select()

    return locals()

@auth.requires_login()
@auth.requires_signature()
def manageProject():
    """
    This controller function is called by the manager to open and close projects
    """
    project = db.project(request.args(0,cast=int))

    if project.status.id in [1,3,4]:
        closed = True
        buttonText = 'Open Bootable'
    else:
        closed = False
        buttonText = 'Close Bootable'

    statusForm = FORM(
        TAG.button(buttonText, _type="submit", _class="btn btn-primary"),
        _action=URL('bootable', 'manageProject', args=[project.id], user_signature=True),
        _style="display: inline-block;"
    )

    if statusForm.process(formname='status').accepted:
        if closed:
            # Not Open -> Open for Pledges
            db.project[project.id] = dict(status = 2)
        else:
            # Open ->
            if project.total >= project.goal:
                # Funded
                db.project[project.id] = dict(status = 3)
            else:
                # Not Funded
                db.project[project.id] = dict(status = 4)

        session.flash = 'Bootable Updated'
        # Reload this object to update all elements
        redirect(URL('bootable', 'manageProject', args=[project.id], user_signature=True))
    elif statusForm.errors:
        response.flash = 'Error updating status'
    else:
        pass

    deleteForm = FORM(
        TAG.button('Delete', _type="submit", _class="btn btn-danger"),
        _action=URL('bootable', 'manageProject', args=[project.id], user_signature=True),
        _style="display: inline-block;"
    )

    if deleteForm.process(formname='delete').accepted:
        db(db.project.id==project.id).delete()
        response.flash = 'Bootable Deleted'
        # Remove this object with jQuery
        response.js =  "jQuery('#%s').remove()" % request.env.http_web2py_component_element
    elif statusForm.errors:
        response.flash = 'Error deleting Bootable'

    return dict(project=project, closed=closed, statusForm=statusForm, deleteForm=deleteForm)

