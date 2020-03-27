#!/bin/bash

chown -R postgres:postgres /etc/postgresql

service postgresql start

tail -f /var/log/postgresql/postgresql-11-main.log