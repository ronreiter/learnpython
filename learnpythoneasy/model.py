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
#

__author__ = 'justin.forest@gmail.com'

from google.appengine.ext import db

class WikiUser(db.Model):
  wiki_user = db.UserProperty()
  joined = db.DateTimeProperty(auto_now_add=True)
  wiki_user_picture = db.BlobProperty()
  user_feed = db.StringProperty()


class WikiContent(db.Model):
  """
  Stores current versions of pages.
  """
  title = db.StringProperty(required=True)
  body = db.TextProperty(required=False)
  author = db.ReferenceProperty(WikiUser)
  updated = db.DateTimeProperty(auto_now_add=True)
  pread = db.BooleanProperty()
  # The name of the page that this one redirects to.
  redirect = db.StringProperty()
  # Labels used by this page.
  labels = db.StringListProperty()
  # Pages that this one links to.
  links = db.StringListProperty()

  @classmethod
  def get_by_key(cls, key):
    return db.get(db.Key(key))


class WikiRevision(db.Model):
  """
  Stores older revisions of pages.
  """
  title = db.StringProperty()
  wiki_page = db.ReferenceProperty(WikiContent)
  revision_body = db.TextProperty(required=True)
  author = db.ReferenceProperty(WikiUser)
  created = db.DateTimeProperty(auto_now_add=True)
  pread = db.BooleanProperty()
