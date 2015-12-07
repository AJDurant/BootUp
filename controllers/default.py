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
    response.title = "Welcome to BootUp"
    response.subtitle = "the next big crowdfunding web application in the UK"

    # Get 5 most recent Bootables
    recent = db(db.project.status != 1).select(orderby=~db.project.id, limitby=(0,5))

    # Get 5 nearest funding
    closest = db(db.project.status != 1).select().sort(lambda row: row.percent(), reverse=True).find(lambda row: row.percent() < 100, limitby=(0,5))

    return locals()

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

        # Put search query in subtitle
        response.subtitle = form.vars.search

        # Get matching categories for search
        catList = [cat['id'] for cat in db(db.category.name.contains(form.vars.search)).select().as_list()]

        # Search db for projects, either from short description or title or category
        query = (
            db.project.category.belongs(catList)
            | db.project.title.contains(form.vars.search)
            | db.project.sdesc.contains(form.vars.search)
        )

        # Get search results - but only projects that have been opened
        results = db(query).select().find(lambda row: row.status != 1)

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
    form = auth()

    if request.args(0) == 'profile':

        # Form to add addresses
        addressForm = SQLFORM(db.address, formstyle='bootstrap3_inline')

        # Set the user to current logged in
        addressForm.vars.userid = auth.user_id

        # Process form
        if addressForm.process().accepted:
            response.flash = 'Address added'
        elif addressForm.errors:
            response.flash = 'Error with address'
        else:
            pass

        # Credit Card form to add cards
        ccForm = SQLFORM(db.cc, formstyle='bootstrap3_inline')

        # Set the user to current logged in
        ccForm.vars.userid = auth.user_id

        # Process form
        if ccForm.process().accepted:
            response.flash = 'Credit card added'
        elif ccForm.errors:
            response.flash = 'Error with credit card'
        else:
            pass

        # Get values after form.process to have the latest data
        # Get Addresses
        addresses = db(db.address.userid==auth.user_id).select()
        # Get Credit cards
        ccs = db(db.cc.userid==auth.user_id).select()

        # Get projects contribuded to
        projects = db(db.project.id==db.pledge.projectid)(db.pledge.userid==auth.user_id).select(db.project.ALL)

        # Set profile title
        response.title = auth.user.realname


    response.subtitle = T( request.args(0).replace('_',' ').capitalize() )

    return locals()

def download():
    return response.download(request, db)
