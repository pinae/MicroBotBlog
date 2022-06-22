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
`projectBlog`. The dependencies are installed conveniently with 
`pip install -r requirements.txt`. Start the development server with 
`python manage.py runserver`.

The web-application is accessible via 
[https://127.0.0.1:8000](https://127.0.0.1:8000). The 
development server restarts automatically when it detects 
changes in the python sourcecode of the project. However for 
some changes like database migrations you need to restart the
server by hand after applying the changes. Check the 
[Django documentation](https://docs.djangoproject.com/en/4.0) 
for more info on that.

## Production setup
The configuration in `settings.py` is already prepared to accept 
environment variables. This makes it easy to create a setup with 
three docker containers. We recommend to use `docker-compose`. Here 
is a snipped from `docker-compose.yml` which illustrates how the 
containers can be configured:

```yaml
version: "3.7"
services:
  pinasprojects:
    build: ./pinasprojects
    container_name: pinasprojects
    restart: always
    volumes:
     - ./pinasprojects/static:/usr/share/nginx/html
     - ./pinasprojects/static:/var/www/static
     - ./pinasprojects/media:/var/www/media
    environment:
     - DJANGO_SECRET_KEY=abcde1234567890abcdefghijklmnopqrstuvwxyz0987654321ABCDEFG
     - DJANGO_DEBUG_MODE=False
     - DJANGO_DB_ENGINE=django.db.backends.mysql
     - DB_NAME=pinasprojects
     - DB_USER=pinasprojects
     - DB_PASSWORD=abcdefg1234567890HIJKLMNOPQRSTU
     - DB_HOST=pinasprojects_maria
     - DB_PORT=3306
     - DJANGO_STATIC_ROOT=/var/www/static
     - DJANGO_STATIC_MEDIA=/var/www/media
     - DJANGO_LANGUAGE_CODE=de-de
     - DJANGO_TIME_ZONE=Europe/Berlin
     - DJANGO_SUPERUSER=admin
     - DJANGO_SUPERUSER_MAIL=mail@example.com
     - DJANGO_SUPERUSER_PASSWORD=plesaeDoNotLeaveThisPasswordUnchanged
    depends_on:
     - pinasprojects_maria
  pinasprojects_nginx:
    image: nginx:alpine
    container_name: pinasprojects-nginx
    restart: always
    volumes:
     - ./pinasprojects/docker-setup/nginx-app.conf:/etc/nginx/conf.d/default.conf:ro
     - ./pinasprojects/static:/usr/share/nginx/html:ro
     - ./pinasprojects/static:/var/www/static:ro
     - ./pinasprojects/media:/var/www/media:ro
     - ./pinasprojects/docker-setup/favicon.svg:/var/www/favicon.svg:ro
    depends_on:
     - pinasprojects
    ports:
     - "127.0.0.1:8510:80"
  pinasprojects_maria:
    image: mariadb:10
    container_name: pinasprojects-maria
    restart: always
    volumes:
      - ./pinasprojects/maria:/var/lib/mysql
    environment:
      - MYSQL_DATABASE=pinasprojects
      - MYSQL_USER=pinasprojects
      - MYSQL_PASSWORD=abcdefg1234567890HIJKLMNOPQRSTU
      - MYSQL_RANDOM_ROOT_PASSWORD=yes
```

In accordance with this file the code of the project lives in a folder `pinasprojects`:
```bash
mkdir pinasprojects
cd pinasprojects
git clone https://github.com/pinae/MicroBotBlog.git .
mkdir maria
cd ..
```
After this you need to pull and build the container with the Django project and the CGI server uWSGI:
```bash
docker compose pull pinasprojects pinasprojects_maria pinasprojects_nginx
docker-compose build pinasprojects
```
The build may take a couple of minutes.

After that you should configure your reverse proxy to pass requests to port `8510`. Here is an example configuration for Nginx:
```nginx
server{
        listen 80;
        listen [::]:80;
        server_name projekte.pinae.net;
        include letsencrypt-webroot;
        location / {
                rewrite        ^ https://$server_name$request_uri? permanent;
        }
}

server{
        listen 443 ssl;
        listen [::]:443 ssl;
        server_name projekte.pinae.net;

        access_log /var/log/nginx/projekte.pinae.net_access.log;
        error_log /var/log/nginx/projekte.pinae.net_error.log;

        ssl_certificate /etc/certificates/projekte.pinae.net/fullchain.pem;
        ssl_certificate_key /etc/certificates/projekte.pinae.net/key.pem;

        ssl_prefer_server_ciphers on;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers 'EECDH+AES:EDH+AES:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!DSS:!RC4:!SEED:!IDEA:!ECDSA';
        ssl_dhparam /etc/nginx/ssl/dhparam.pem;

        include letsencrypt-webroot;

        location / {
                proxy_pass      http://127.0.0.1:8510;
        }
}
```
Do not forget to issue SSL certificates. We did this with `acme.sh` and Let's Encrypt.

After that you can start the containers with
```bash
docker compose up -d pinasprojects pinasprojects_maria pinasprojects_nginx
```

### Updating the production setup
```bash
docker-compose rm -s pinasprojects pinasprojects_maria pinasprojects_nginx
cd pinasprojects
git pull
cd ..
docker-compose build pinasprojects
docker-compose up -d pinasprojects pinasprojects_maria pinasprojects_nginx
```

If there are errors concerning insufficient rights to write to the folder `pinasprojects/maria` change the ownership to your user while leaving the group untouched. The user IDs in the container and in the host system may differ and the files need to be writable for both user IDs.

