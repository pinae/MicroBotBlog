FROM debian:bullseye
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y apt-utils && \
    apt-get install -y \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	libmariadbclient-dev-compat && \
	pip3 install uwsgi mysqlclient && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt /home/docker/requirements.txt
COPY projectBlog /var/www/
COPY docker-setup/uwsgi-app.ini /etc/uwsgi/apps-enabled/uwsgi-app.ini
COPY docker-setup/init_and_run.sh /home/docker/init_and_run.sh
WORKDIR /home/docker/
RUN pip3 install -r requirements.txt
EXPOSE 3031
CMD ["/home/docker/init_and_run.sh"]
