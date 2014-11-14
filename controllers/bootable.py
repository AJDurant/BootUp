"""
This is the bootable controller
 - project displays project information
 - create is used to create new projects
 - edit is used to update projects and add reward goals
 - manager is used to view a users bootables and access edit for them


"""

def project():
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
        response.flash = 'Project Submitted'
        # Redirect to edit page for adding rewards
        # TODO
    elif form.errors:
        response.flash = 'Error with form'
    else:
        pass

    return dict(form=form)


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

    if project.manager != auth.user_id:
        redirect(URL('default', 'index'))

    # Setup form, using bootstrap style - not tables!
    editform = SQLFORM(db.project, project, formstyle='bootstrap3_inline')

    # Set page title
    response.title = 'Edit Bootable: ' + project.title

    return dict(editform=editform)

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
