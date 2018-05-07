# Sleepmap Routing
This is the routing backend of the [sleepmap](https://github.com/sdhoek/sleepmap) project.

Pgrouting is used for calculating routes. The netwerk topology is imported from the openstreetmap.

## Dependencies
You'll need to download the .osm file of the area of interest yourself. Try the [bbbike.org](http://download.bbbike.org/osm/bbbike/) database.

To run the docker container your host system need to have [docker](https://www.docker.com/) and [docker compose](https://docs.docker.com/compose/) installed.

## Configuration
Relevant configuration options can ben controlled in the .env file. Of note are the configuration options `INPUT_OSM` and `INPUT_VIEWSHEDS`. Please make sure the correct filenames for the files that belong to your area of interest are provided in the .env file and in the `/app/src/data` directory.

By default the docker container is bound to `127.0.0.1:8000`. You can change this in the docker-compose.yml file.

## Setup

### Build container
Build the container with the included script
```
./build.sh
```

### Load the data in the database
A single script is provided that performs the neccesary import steps
```
./setup.sh
```
This step might take a while

### Start
Start the docker container with the following command
```
docker-compose up
```
Or to start in the background (deamon mode)
```
docker-compose up -d
```

### Expose to web
By default the routing backend will now be running on port 8000. You'll need to proxy traffic to the backend application through a proper webserver such as apache.

## API
This application exposes a single endpoint `/api/route`.

### POST /api/route
Request Content type: application/json

Request body description:
```json
{
    "start": <GeoJSON.Point>,
    "end": <GeoJSON.Point>,
    "privacy": <boolean>
}
```

Request body example:
```json
{
    "start":{
        "type":"Feature",
        "geometry":{
        "type":"Point",
        "coordinates":[
            5.082,
            52.084
        ]
        }
    },
    "end":{
        "type":"Feature",
        "geometry":{
        "type":"Point",
        "coordinates":[
            5.14,
            52.105
        ]
        }
    },
    "privacy":false
}
```

