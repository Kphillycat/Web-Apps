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
import os
import webapp2

import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(autoescape=True,
loader = jinja2.FileSystemLoader(template_dir))

class Blog(db.Model):
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw): 
        self.write(self.render_str(template, **kw))
	
class MainPage(Handler):
	def render_front(self, title="", content="", error=""):
		blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
		self.render("front.html", title = title, content = content, error = error, blogs = blogs)
		
	def get(self):
		self.render_front()

	
class BlogEntryPage(Handler):
	def render_blog_entry(self, title="", content="", error=""):
		blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
		self.render("blogentry.html", title = title, content = content, error = error, blogs = blogs)
		
	def get(self):
		self.render("blogentry.html")
		
	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")
		
		if subject and content:	
			full_blog = Blog(title = subject, content = content)
			full_blog.put()
			self.redirect("/blogview/%s" %(full_blog.key().id()))
		
		else:
			error = "we need both title and content"
			self.render_blog_entry(error = error)
		
class BlogViewPage(Handler):
	def render_single(self,title="",content=""):
		self.render("blogview.html", title = title, content = content)
		
	def get(self,id):
		blog = Blog.get_by_id(int(id))
		#blog = db.GqlQuery("SELECT * from Blog ORDER BY created DESC LIMIT 1")
		self.render("blogview.html", blog = blog)
			
app = webapp2.WSGIApplication([('/', MainPage), ('/newpost',BlogEntryPage), ('/blogview/(\d+)',BlogViewPage)], debug=True)	