"""
This module provides an override for Auth.navbar() to fix the dropdown menu

The dropdown menu could not be toggled once a user was logged in, as the
correct classes were not being applied.


"""



import base64
try:
    import cPickle as pickle
except:
    import pickle
import datetime
import thread
import logging
import copy
import sys
import glob
import os
import re
import time
import traceback
import smtplib
import urllib
import urllib2
import Cookie
import cStringIO
import ConfigParser
import email.utils
import random
from email import MIMEBase, MIMEMultipart, MIMEText, Encoders, Header, message_from_string, Charset

from gluon.contenttype import contenttype
from gluon.storage import Storage, StorageList, Settings, Messages
from gluon.utils import web2py_uuid
from gluon.fileutils import read_file, check_credentials
from gluon import *
from gluon.contrib.autolinks import expand_one
from gluon.contrib.markmin.markmin2html import \
    replace_at_urls, replace_autolinks, replace_components
from gluon.dal import Row, Set, Query

import gluon.serializers as serializers

try:
    # try stdlib (Python 2.6)
    import json as json_parser
except ImportError:
    try:
        # try external module
        import simplejson as json_parser
    except:
        # fallback to pure-Python module
        import gluon.contrib.simplejson as json_parser

from gluon.tools import Auth

DEFAULT = lambda: None

class myAuth(Auth):

    # override auth.navbar() due to dropdown toggle error
    def navbar(self, prefix='Welcome', action=None,
               separators=(' [ ', ' | ', ' ] '), user_identifier=DEFAULT,
               referrer_actions=DEFAULT, mode='default'):
        """ Navbar with support for more templates
        This uses some code from the old navbar.

        Args:
            mode: see options for list of

        """
        items = []  # Hold all menu items in a list
        self.bar = ''  # The final
        T = current.T
        referrer_actions = [] if not referrer_actions else referrer_actions
        if not action:
            action = self.url(self.settings.function)

        request = current.request
        if URL() == action:
            next = ''
        else:
            next = '?_next=' + urllib.quote(URL(args=request.args,
                                                vars=request.get_vars))
        href = lambda function: '%s/%s%s' % (action, function, next
                                             if referrer_actions is DEFAULT
                                             or function in referrer_actions
                                             else '')
        if isinstance(prefix, str):
            prefix = T(prefix)
        if prefix:
            prefix = prefix.strip() + ' '

        def Anr(*a, **b):
            b['_rel'] = 'nofollow'
            return A(*a, **b)

        if self.user_id:  # User is logged in
            logout_next = self.settings.logout_next
            items.append({'name': T('Log Out'),
                          'href': '%s/logout?_next=%s' % (action,
                                                          urllib.quote(
                                                          logout_next)),
                          'icon': 'icon-off'})
            if not 'profile' in self.settings.actions_disabled:
                items.append({'name': T('Profile'), 'href': href('profile'),
                              'icon': 'icon-user'})
            if not 'change_password' in self.settings.actions_disabled:
                items.append({'name': T('Password'),
                              'href': href('change_password'),
                              'icon': 'icon-lock'})

            if user_identifier is DEFAULT:
                user_identifier = '%(first_name)s'
            if callable(user_identifier):
                user_identifier = user_identifier(self.user)
            elif ((isinstance(user_identifier, str) or
                  type(user_identifier).__name__ == 'lazyT') and
                  re.search(r'%\(.+\)s', user_identifier)):
                user_identifier = user_identifier % self.user
            if not user_identifier:
                user_identifier = ''
        else:  # User is not logged in
            items.append({'name': T('Log In'), 'href': href('login'),
                          'icon': 'icon-off'})
            if not 'register' in self.settings.actions_disabled:
                items.append({'name': T('Sign Up'), 'href': href('register'),
                              'icon': 'icon-user'})
            if not 'request_reset_password' in self.settings.actions_disabled:
                items.append({'name': T('Lost password?'),
                              'href': href('request_reset_password'),
                              'icon': 'icon-lock'})
            if (self.settings.use_username and not
                    'retrieve_username' in self.settings.actions_disabled):
                items.append({'name': T('Forgot username?'),
                             'href': href('retrieve_username'),
                             'icon': 'icon-edit'})

        def menu():  # For inclusion in MENU
            self.bar = [(items[0]['name'], False, items[0]['href'], [])]
            del items[0]
            for item in items:
                self.bar[0][3].append((item['name'], False, item['href']))

        def bootstrap3():  # Default web2py scaffolding
            def rename(icon): return icon+' '+icon.replace('icon','glyphicon')
            self.bar = UL(LI(Anr(I(_class=rename('icon '+items[0]['icon'])),
                                 ' ' + items[0]['name'],
                                 _href=items[0]['href'])),_class='dropdown-menu')
            del items[0]
            for item in items:
                self.bar.insert(-1, LI(Anr(I(_class=rename('icon '+item['icon'])),
                                           ' ' + item['name'],
                                           _href=item['href'])))
            self.bar.insert(-1, LI('', _class='divider'))
            if self.user_id:
                self.bar = LI(Anr(prefix, user_identifier,
                                  _href='#',_class="dropdown-toggle",   # These lines are the edit to make
                                  data={'toggle':'dropdown'}),          # the navbar dropdown work correctly
                              self.bar,_class='dropdown')
            else:
                self.bar = LI(Anr(T('Log In'),
                                  _href='#',_class="dropdown-toggle",
                                  data={'toggle':'dropdown'}), self.bar,
                              _class='dropdown')

        def bare():
            """ In order to do advanced customization we only need the
            prefix, the user_identifier and the href attribute of items

            Examples:
                Use as::

                # in module custom_layout.py
                from gluon import *
                def navbar(auth_navbar):
                    bar = auth_navbar
                    user = bar["user"]

                    if not user:
                        btn_login = A(current.T("Login"),
                                      _href=bar["login"],
                                      _class="btn btn-success",
                                      _rel="nofollow")
                        btn_register = A(current.T("Sign up"),
                                         _href=bar["register"],
                                         _class="btn btn-primary",
                                         _rel="nofollow")
                        return DIV(btn_register, btn_login, _class="btn-group")
                    else:
                        toggletext = "%s back %s" % (bar["prefix"], user)
                        toggle = A(toggletext,
                                   _href="#",
                                   _class="dropdown-toggle",
                                   _rel="nofollow",
                                   **{"_data-toggle": "dropdown"})
                        li_profile = LI(A(I(_class="icon-user"), ' ',
                                          current.T("Account details"),
                                          _href=bar["profile"], _rel="nofollow"))
                        li_custom = LI(A(I(_class="icon-book"), ' ',
                                         current.T("My Agenda"),
                                         _href="#", rel="nofollow"))
                        li_logout = LI(A(I(_class="icon-off"), ' ',
                                         current.T("logout"),
                                         _href=bar["logout"], _rel="nofollow"))
                        dropdown = UL(li_profile,
                                      li_custom,
                                      LI('', _class="divider"),
                                      li_logout,
                                      _class="dropdown-menu", _role="menu")

                        return LI(toggle, dropdown, _class="dropdown")

                # in models db.py
                import custom_layout as custom

                # in layout.html
                <ul id="navbar" class="nav pull-right">
                    {{='auth' in globals() and \
                      custom.navbar(auth.navbar(mode='bare')) or ''}}</ul>

            """
            bare = {}

            bare['prefix'] = prefix
            bare['user'] = user_identifier if self.user_id else None

            for i in items:
                if i['name'] == T('Log In'):
                    k = 'login'
                elif i['name'] == T('Sign Up'):
                    k = 'register'
                elif i['name'] == T('Lost password?'):
                    k = 'request_reset_password'
                elif i['name'] == T('Forgot username?'):
                    k = 'retrieve_username'
                elif i['name'] == T('Log Out'):
                    k = 'logout'
                elif i['name'] == T('Profile'):
                    k = 'profile'
                elif i['name'] == T('Password'):
                    k = 'change_password'

                bare[k] = i['href']

            self.bar = bare

        options = {'asmenu': menu,
                   'dropdown': bootstrap3,
                   'bare': bare
                   }  # Define custom modes.

        if mode in options and callable(options[mode]):
            options[mode]()
        else:
            s1, s2, s3 = separators
            if self.user_id:
                self.bar = SPAN(prefix, user_identifier, s1,
                                Anr(items[0]['name'],
                                _href=items[0]['href']), s3,
                                _class='auth_navbar')
            else:
                self.bar = SPAN(s1, Anr(items[0]['name'],
                                _href=items[0]['href']), s3,
                                _class='auth_navbar')
            for item in items[1:]:
                self.bar.insert(-1, s2)
                self.bar.insert(-1, Anr(item['name'], _href=item['href']))

        return self.bar
