"""
This is the main application controller
 - index is the default action of any application
 - user is required for authentication and authorization


"""

def index():
    """
    Home Page

    BootUp will have a home page that shows the 5 most recently created projects
    and the 5 projects closest to their funding goal.
    """
    # Set page title
    response.title = "BootUp"
    response.subtitle = "the next big crowdfunding web application in the UK"

    return dict()

def search():
    """
    Searches

    People interested in pledging should be able to search from any page for projects of
    interest. They should be able to search for words in the title or in the short description.
    People interested in pledging should be able to search by category of project and receive
    a list of projects back in that category. The following is the complete list of categories to
    which a project can belong:
    Art, Comics, Crafts, Fashion, Film, Games, Music, Photography, Technology
    """
    # Set page title
    response.title = 'Search Results:'

    form = FORM(
        DIV(
            LABEL('Search', _class="sr-only", _for="search"),
            INPUT(_type="text", _name="search", _placeholder="Search", _class="form-control"),
            _class="form-group"
        ),
        TAG.button(
            SPAN(_class="glyphicon glyphicon-search"),
            _type="submit",
            _class="btn btn-default"),
        _class="navbar-form navbar-right",
        _role="search",
        _action=URL('default', 'search', extension=''))

    if form.accepts(request,session):
        response.flash = 'Search successful!'
        # Put search query in subtitle
        response.subtitle = form.vars.search
        # Search db for projects, either from short description, title or category
        # TODO
        results = form.vars.search
    elif form.errors:
        response.flash = 'Search has errors!'
        results = None
    else:
        results = None
    return dict(form = form, results = results)

# Default web2py User function
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

