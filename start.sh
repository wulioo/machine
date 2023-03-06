#! /bin/bash
groupadd -r zdh -g 1001 && useradd -r -u 1001 -g zdh zdh && chown -R 1001:1001  /var/www/html/machine  /var/run/celery;
exec gosu zdh bash -l -c "uwsgi --ini uwsgi.ini && celery -A Machine worker  -l INFO"
