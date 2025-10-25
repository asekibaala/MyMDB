FROM phusion/baseimage:latest

RUN mkdir /mymdb
WORKDIR /mymdb
COPY requirements* /mymdb/
COPY django/ /mymdb/django/
COPY scripts/ /mymdb/scripts/
RUN mkdir /var/log/mymdb
RUN touch /var/log/mymdb/gunicorn.log
