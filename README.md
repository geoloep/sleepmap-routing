Setup
-----

./build.sh

get Utrecht.osm in app/src/data.

`docker-compose run --service-ports --rm django bash /app/data/inladen.sh` -- imports Utrecht.osm and viewsheds (viewsheds: TODO).

modify data: `docker-compose run --service-ports --rm django psql -h postgresql -U postgres -d routing -c 'create index geo_idx_ways on ways using gist (the_geom);'`
add the viewsheds table: `docker-compose run --service-ports --rm django ogr2ogr -f "PostgreSQL" PG:"dbname=routing host=postgresql user=postgres" "/app/data/viewsheds_25meter_v3.json" -nln viewsheds`
add camera cost column: `docker-compose run --service-ports --rm django psql -h postgresql -U postgres -d routing -c 'alter table ways add column camera integer;`
fill camera cost column: `docker-compose run --service-ports --rm django python3 /app/data/cameras.py`

