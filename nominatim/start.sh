#!/bin/bash

chown -R root /etc/postgresql
chown -R postgres:postgres /var/log/postgresql
chmod -R go+rw /var/log/postgresql

stopServices() {
        service apache2 stop
        service postgresql stop
}
trap stopServices TERM

service postgresql start
service apache2 start

# fork a process and wait for it
tail -f /var/log/postgresql/postgresql-11-main.log &
wait
