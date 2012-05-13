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
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
name = ""
                      
def valid_us(name):
    return USER_RE.match(name)
def valid_pw(pw):
    return PASSWORD_RE.match(pw)
def valid_email(email):
    return EMAIL_RE.match(email)
    
    

form="""
<form method="post">
    <table>
    <tr>
        <td>Username</td>
        <td><input type="text" name="username" value="%(us)s"></td>
        <td><div style= color:red>%(us_error)s</div></td>
    </tr>
    <tr>
        <td>Password</td>
        <td><input type="password" name="password" value="%(pass)s"></td>
        <td><div style= color:red>%(pw_error)s</div></td>
    </tr>
    <tr>
        <td>Verify Password</td>
        <td><input type="password" name="verify" value="%(pass2)s"></td>
        <td><div style= color:red>%(pw_match_error)s</div></td>
    </tr>
    <tr>
        <td>Email (optional)</td>
        <td><input type="text" name="email" value="%(em)s"></td>
        <td><div style= color:red>%(em_error)s</div></td>
    </tr>
    </table>
    <input type="submit">
</form>
"""
    
    
class MainHandler(webapp2.RequestHandler):
    def write_form(self, us_e="", us="", pw="", pw2="", email="", pw_e="", em_e="", pw_match_error=""):
        self.response.out.write(form % {"us_error": us_e, "us" : us, "pass" :pw, "pass2" : pw2, "em" : email, "em_error" : em_e, "pw_error" : pw_e,
                                        "pw_match_error" : pw_match_error})

    def get(self):
        self.write_form()

    def post(self):
        name_error =""
        pass_error=""
        email_error=""
        match_error=""
		
		#default email validity to True since it's optional
        em_valid = True
		
		#grab data from form
        name = self.request.get('username')
        password = self.request.get('password')
        password_2 = self.request.get('verify')
        email = self.request.get('email')
        
		#valid the username and password using regular expressions
        us_valid = valid_us(name)
        pw_valid = valid_pw(password)

        if password != password_2:
                match_error = "Your passwords didn't match."
                match_valid = False
        else:
            match_valid = True

        if email:
            em_valid = valid_email(email)

        if(us_valid and pw_valid and em_valid and match_valid):
			#Successful registration results in a welcome page for the user. Name is added to the URL
            self.redirect("/welcome?username=%s" %(name))

            
        else:
            if not us_valid:
                name_error = "That's not a valid username."
            if not pw_valid:
                pass_error = "That wasn't a valid password."
            if not em_valid:
                email_error = "That wasn't a valid email."
            
                
            self.write_form(name_error,name,"","",email,pass_error,email_error,match_error)
            
class SuccessHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('username')
        self.response.out.write("Welcome, %s!" %name)
        
        

    

app = webapp2.WSGIApplication([('/', MainHandler),('/welcome',SuccessHandler)],
                              debug=True)
