#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
DEVELOPER_MAIL = "shinichiro.su@gmail.com"

import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
# from django.utils import simplejson as json
import logging
import inspect
import webapp2
import json
import hashlib
from model import *

#
# decorators
#
def login_required(function):
    def _loging_required(arg):
        user = users.get_current_user()
        if not user:
            arg.redirect(users.create_login_url(arg.request.uri))

        arg.user = user
        res = function(arg)
        return res
    return _loging_required

#
# RequestHandler
#
class IndexHandler(webapp2.RequestHandler):
    @login_required
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'template/index.html')
        self.response.out.write(template.render(path, {}))

class TaskHandler(webapp2.RequestHandler):
    @login_required
    def get(self):
        pass
#         tasks = Task.all().filter('user =', self.user)

#         path = os.path.join(os.path.dirname(__file__), 'template/index.html')
#         self.response.out.write(template.render(path, {tasks:tasks}))

    @login_required
    def post(self):
        logging.info(self.request.POST)
        task = Task(user = self.user, name = self.request.get('task'))
        task.put()
#         self.redirect('/')

class TaskListHandler(webapp2.RequestHandler):
    @login_required
    def get(self):
        tasks = Task.all().filter('user =', self.user).order('-created_at').fetch(100)
        logging.debug(tasks)
#         tasks_json = [{'name':t.name, 'created_at':t.created_at.strftime('%Y-%m-%d %H:%M:%S')} for t in tasks]
#         logging.info(tasks_json)
#         logging.info(Task.jsonize(tasks))

        self.response.out.write(Task.jsonize(tasks))

app = webapp2.WSGIApplication([('/', IndexHandler),
                               ('/task', TaskHandler),
                               ('/tasklist', TaskListHandler),
                               ],
                              debug=True)
