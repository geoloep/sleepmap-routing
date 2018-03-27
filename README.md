Setup
-----

./build.sh

get Utrecht.osm in app/src/data.

`docker-compose run --service-ports --rm django bash /app/data/inladen.sh` -- imports Utrecht.osm and viewsheds (viewsheds: TODO).

modify data: `docker-compose run --service-ports --rm django psql -h postgresql -U postgres -d routing -c 'create index geo_idx_ways on ways using gist (the_geom);'`

add camera cost column: `docker-compose run --service-ports --rm django python /app/src/data/cameras.py`
