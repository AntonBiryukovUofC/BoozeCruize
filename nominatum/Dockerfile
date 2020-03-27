FROM mediagis/nominatim:3.4
WORKDIR /
RUN mkdir /data
COPY nominatim_data_calgary/ /data/
RUN /bin/sh /app/init.sh /data/calgary_metro.osm.pbf postgresdata 4