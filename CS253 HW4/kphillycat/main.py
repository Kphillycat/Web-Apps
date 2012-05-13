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
import re
import hashlib

import jinja2

from google.appengine.ext import db

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
name = ""

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(autoescape=True,
loader = jinja2.FileSystemLoader(template_dir))

class User(db.Model):
	name = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.StringProperty(required = False)
                      
def valid_us(name):
    return USER_RE.match(name)
def valid_pw(pw):
    return PASSWORD_RE.match(pw)
def valid_email(email):
    return EMAIL_RE.match(email)
	
def hash_str(s):
	#hashes the string s
	return hashlib.sha256(s).hexdigest()
	
def make_secure_val(s):
	#returns hash of s and s in the format "s|hash(s)"
	return "%s|%s" % (s,hash_str(s))

def check_secure_val(h):
	#validates h is a valid s|hash(s)
	val = h.split('|')[0]
	#grab s portion of h
	if h == make_secure_val(val):
		#return the True if the cookie hasn't been tampered with
		return True


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw): 
        self.write(self.render_str(template, **kw))
	
class MainPage(Handler):
	def render_reg(self, us_e="", us="", pw="", pw2="", email="", pw_e="", em_e="", pw_match_error=""):
		self.render("registration.html", us_error = us_e, us = us, password = pw, pass2 = pw2, em = email, em_error = em_e, pw_error = pw_e, pw_match_error = pw_match_error)
	
	def get(self):
		#Get request grabs the registration form html with all parameters defaulted to blank
		self.render_reg()
		user_cookie_val = self.request.cookies.get('user')
		
		if user_cookie_val:
			#user has been here before
			cookie_val = check_secure_val(user_cookie_val)
			if cookie_val:
				self.redirect("/welcome")

		
	def post(self):		
			#Post request validates the input and puts it into the database
			name_error =""
			pass_error=""
			email_error=""
			match_error=""
			
			#Easier to default email valid to true b/c it's optional
			em_valid = True
			
			#Grab all the values from the HTML form
			name = self.request.get('username')
			password = self.request.get('password')
			password_2 = self.request.get('verify')
			email = self.request.get('email')
			
			#validate username and password using regular expressions
			us_valid = valid_us(name)
			pw_valid = valid_pw(password)			
			
			#Query the database for the user
			que = db.Query(User).filter("name =", name).fetch(limit=1)
			#Use the results of the query to see if the user exists already
			if que:
				name_error = "That user already exists"
				us_valid = False

			if password != password_2:
					match_error = "Your passwords didn't match."
					match_valid = False
			else:
				match_valid = True

			#If the user does decide to provide an email we need to check it against regular expressions
			if email:
				em_valid = valid_email(email)
			
			if(us_valid and pw_valid and em_valid and match_valid):
				#Successful user registration put entry in database
				full_reg = User(name = name,password = password,email = email)
				full_reg.put()
				#set hash value of cookie based on username in s|hash(s) format, had to force str was getting unicode error
				hash_user_cookie = str(make_secure_val(name))
				self.response.headers.add_header('Set-Cookie', 'user = %s; Path=/' % (hash_user_cookie))
				self.redirect("/welcome")

			#Checks each valid state and applies the appropriate error message	
			else:
				#If user name already in the database don't override the error
				if not us_valid and not name_error:
					name_error = "That's not a valid username."
				if not pw_valid:
					pass_error = "That wasn't a valid password."
				if not em_valid:
					email_error = "That wasn't a valid email."

				#entry page renders with all the appropriate error messages			
				self.render_reg(name_error,name,"","",email,pass_error,email_error,match_error)
		
		
            
class SuccessHandler(Handler):
    def get(self):
		#Grab the user name from the cookie
		user_cookie_val = self.request.cookies.get('user')
		
		#check to see if there is a user cookie
		if not user_cookie_val:
			self.redirect("/signup")
		
		#Split it to only get the username portion
		name = user_cookie_val.split('|')[0]
		self.response.out.write("Welcome, %s!" %name)
		
class LoginHandler(Handler):
	def render_login(self,username_error="",password_error=""):
		self.render("login.html", username_error = username_error, password_error = password_error)
		
	def get(self):
		self.render_login()
	
	def post(self):
		username_error = ""
		password_error = ""
		
		name = self.request.get('username')
		pw = self.request.get('password')
		
		#query the database where the name is equal to name
		a = db.GqlQuery('SELECT * FROM User WHERE name = :1', name)
		que = a.get()
		
		if que:
			#Then the username is in the database we just have to check that the password if correct
			if que.password == pw:
				hash_user_cookie = str(make_secure_val(name))
				self.response.headers.add_header('Set-Cookie', 'user = %s; Path=/' % (hash_user_cookie))
				self.redirect("/welcome")
			
			else:
				#password is invalid
				password_error = "Password is invalid"
				
		
		else:
			#user is not in database
			username_error = "That user doesn't exist"
			
		self.render_login(username_error,password_error)
		
class LogoutHandler(Handler):
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'user=; Path=/')
		self.redirect("/signup")
		


app = webapp2.WSGIApplication([('/signup', MainPage), ('/welcome',SuccessHandler), ('/login',LoginHandler), ('/logout',LogoutHandler)], 
                              debug=True)
