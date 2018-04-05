Installation
------------

```
./build
```

builds the django/client docker image.

Data
----
* Download {Utrecht}: http://download.bbbike.org/osm/bbbike/Utrecht/ and extract it: `gunzip Utrecht.osm.gz`.
* You also need the camera data as geojson.


start the database container: `docker-compose up -d postgresql`.

import the data: `docker-compose run django import.sh`

process the data: `docker-compose run django process.sh`


Run
---

Start the web server: `docker-compose up -d django`


Clean
-----

```
docker-compose run django clean.sh
```
