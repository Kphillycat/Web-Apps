For CS253 HW4 part 1, we had to create a user registration page. It's similar to HW 2 where there's a sign up 
form with proper error handling, except this time we have to check if the user name already exists and also
set a cookie for the current user. I implemented this by using GAE's datastore to hold the user info
and verified the cookie by checking it against a (non-salted) SHA256 hash. 

The second portion of this app is for logging in and setting a cookie. When the user goes to '/login' if they have already 
signed up ('/signup') they can log in. Errors are produced when the username is not found or the password is incorrect.

The third part of this app enabled the user to logout ('/logout'). When the user navigates to the logout page the cookie
it cleared and is redirected to the signup page ('/signup')

As always, the html files are located in the "kphillycat/templates" folder and the python is written the main.py 
file in "kphillycat" folder. 

Note: This webapp assumes the first page's path is '/signup' not '/'