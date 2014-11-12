# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    """
    Home Page

    BootUp will have a home page that shows the 5 most recently created projects
    and the 5 projects closest to their funding goal.
    """

    return dict()


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

    project = db.project(request.args(0,cast=int)) or redirect(URL('index'))

    return dict()



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

