FROM phusion/baseimage:latest

RUN mkdir /mymdb
WORKDIR /mymdb
COPY requirements* /mymdb/
COPY django/ /mymdb/django/
COPY scripts/ /mymdb/scripts/
RUN mkdir /var/log/mymdb
RUN touch /var/log/mymdb/gunicorn.log
RUN apt-get update && apt-get install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
RUN pip3 install --upgrade pip
RUN virtualenv /mymdb/venv
RUN /mymdb/scripts/pip_install.sh /mymdb
