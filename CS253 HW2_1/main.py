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
import webapp2
import cgi

def escape_html(input):
	return cgi.escape(input, quote=True)

form="""
<form method="post">
	<textarea name="text"
                style="height: 100px; width: 400px;" >%(q)s</textarea>
      <br>
	<input type="submit">	
</form>
"""

class MainHandler(webapp2.RequestHandler):	
	def write_form(self,q=""):
		self.response.out.write(form % {"q": escape_html(q.encode('rot13'))})
	
	def get(self):
		self.write_form()
		#get draws the form
	
	def post(self):
		user_q=self.request.get('text')		
		self.write_form(user_q)
		
app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
