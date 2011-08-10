# -*- coding: utf-8 -*-
#
# Copyright 2008 Google Inc. All Rights Reserved.
#
# Licensed under the GNU General Public License, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.gnu.org/licenses/gpl.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Python imports.
import urllib
import logging

# GAE imports.
from google.appengine.ext import webapp

register = webapp.template.create_template_register()

@register.filter
def uurlencode(value):
    if type(value) == unicode:
        value = value.encode('utf-8')
    try:
        if type(value) != str:
            raise Exception('got \"%s\" instead of a string.' % value.__class__.__name__)
        return urllib.quote(value)
    except Exception, e:
        logging.error('Error in the uurlencode filter: %s' % e)
        return ''


@register.filter
def pageurl(value):
    if type(value) == unicode:
        value = value.encode('utf-8')
    elif type(value) != str:
        value = str(value)
    return '/' + urllib.quote(value.replace(' ', '_'))

@register.filter
def labelurl(value):
    if type(value) == unicode:
        value = value.encode('utf-8')
    elif type(value) != str:
        value = str(value)
    return '/Label:' + urllib.quote(value.replace(' ', '_'))


@register.filter
def hostname(value):
    host = value.split('/')[2]
    if host.startswith('www.'):
        host = host[4:]
    return host


@register.filter
def nonestr(value):
    if value is None:
        return ''
    return value
