# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

"""
This model creates the menu for the app



"""

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(
                    B('BootUp'),
                    _class="navbar-brand",
                    _href="/BootUp"
                )
response.title = 'BootUp'
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Andy Durant'
response.meta.keywords = 'BootUp, bootable, crowdsource, funding'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    ('Home', False, URL('default', 'index'), []),
    ('Create Bootable', False, URL('bootable', 'create'), []),
    ('Manage Bootables', False, URL('bootable', 'manager'), [])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [

        ]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
