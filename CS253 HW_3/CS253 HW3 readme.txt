In CS253 Homework #3 we had to simply create a blog. This consisted of having page where the user could enter in
a new blog entry (path = '/newpost'), a view of that single blog post (path = '/blogview') and
the view of all the blogs entered on one page descending with latest post on top (path ='/'). I did this
utilizing Google App Engine's datastore and jinja2 for html template support.

HTML is stored in the "kphillycat/templates" folder and the main.py is in the "kphillycat" folder. 