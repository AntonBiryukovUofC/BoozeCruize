#!/bin/bash

sudo -u postgres psql postgres -tAc "GRANT usage ON SCHEMA public TO 'www-data';"
sudo -u postgres psql postgres -tAc "GRANT SELECT ON ALL TABLES IN SCHEMA public TO 'www-data';"

service postgresql start
tail -f /var/log/postgresql/postgresql-11-main.log