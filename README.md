# MicroBotBlog
Microblog-Website implemented with Django. Content can be 
submitted with a messenber bot.

## Development Setup
You do not need to install a big webserver and database 
for development and testing. Django includes a slow webserver 
for development purposes. Check out the project with 
`git clone https://github.com/pinae/MicroBotBlog.git`
and navigate to the newly created folder `MicroBotBlog`.

You may want to initialize a new virtualenv with 
`python3 -m venv env`. This virtualenv is optional but isolates
the django project from the system-wide Python installation. 
This isolation makes sense on most Linux systems and on macOS 
and Windows if you develop different python projects at the same 
time. Activate the virtualenv on Unix-style systems with 
`source env/bin/activate`.

After activating the virtualenv navigate to the folder 
`projectBlog`. Start the development server with 
`python manage.py runserver`.

The web-application is accessible via 
[https://127.0.0.1:8000](https://127.0.0.1:8000). The 
development server restarts automatically when it detects 
changes in the python sourcecode of the project. However for 
some changes like database migrations you need to restart the
server by hand after applying the changes. Check the 
[Django documentation](https://docs.djangoproject.com/en/4.0) 
for more info on that.