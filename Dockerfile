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

#collect static files
RUN bash /mymdb/scripts/collect_static.sh /mymdb

# add nginx config
COPY nginx/mymdb.conf /etc/nginx/sites-available/mymdb.conf
RUN rm /etc/nginx/sites-enabled/*
RUN ln -s /etc/nginx/sites-available/mymdb.conf /etc/nginx/sites-enabled/mymdb.conf
COPY runit/nginx /etc/service/nginx/run

#configure uwsgi
COPY uwsgi/mymdb.ini /etc/uwsgi/apps-enabled/mymdb.ini
RUN mkdir -p /var/log/uwsgi 
RUN touch /var/log/uwsgi/mymdb.log
RUN chown www-data /var/log/uwsgi/mymdb.log
 
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EXPOSE 80  


