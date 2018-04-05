cd /app
for d in ls data/*.osm; do
    osm2pgrouting -f $d --conf importconfig.xml --dbname routing --username postgres --host postgresql
done
