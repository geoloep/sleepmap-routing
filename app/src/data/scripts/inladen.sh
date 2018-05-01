osm2pgrouting -f /app/data/$INPUT_OSM --conf /app/data/scripts/$PGROUTING_CONFIG --dbname routing --username postgres --clean --host postgresql

psql -U postgres -h postgresql -d routing -c 'ALTER TABLE ways ADD COLUMN camera integer;'