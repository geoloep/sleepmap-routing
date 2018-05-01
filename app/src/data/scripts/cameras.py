import psycopg2
from json import load, dumps
from os import environ

# This script intersects the camera viewsheds with ways and updates the camera field accordingly

print('Intersecting camera viewsheds')

conn = psycopg2.connect("host=postgresql dbname=routing user=postgres")
cur = conn.cursor()

# Reset camera counter
cur.execute("""
update public.ways
set camera = 0
""")

conn.commit()

print('Camera counter reset')

with open('/app/data/' + environ.get('INPUT_VIEWSHEDS')) as jsonfile:
    geojson = load(jsonfile)

    for feature in geojson['features']:
        q = """
        with ways as (
            select gid, the_geom from ways)
        select gid from ways where ST_Intersects(ways.the_geom, ST_SetSRID(ST_GeomFromGeoJSON('{}'), 4326))
        """.format(dumps(feature['geometry']))

        try:
            cur.execute(q)
        except Exception as e:
            print(e)
            print('Illegal geometry:', dumps(feature['geometry']))
            conn.rollback()
            continue

        results = cur.fetchall()

        print('ID {}; hits {}'.format(feature['properties']['id'], results))

        if len(results) > 0:

            for gids in results:
                for gid in gids:
                    # print(gid)
                    q = """
                    update ways
                        set camera = camera + 1
                    where gid = '{}'
                    """.format(gid)

                    cur.execute(q)

            conn.commit()

conn.close()
