import psycopg2
from json import loads


class RouteHelper():

    def __init__(self):
        self.conn = self.get_conn()

    def get_conn(self):
        return psycopg2.connect("host=postgresql dbname=routing user=postgres")

    def get_curr(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def test(self):
        cur = self.get_curr()
        cur.execute("""
        SELECT * FROM pgr_dijkstra(
        'SELECT gid AS id,
            source,
            target,
            length AS cost
            FROM ways',
        128, 228,
        directed := false);""")

        r = cur.fetchall()

        return r

    def get_node(self, lng, lat):
        cur = self.get_curr()

        cur.execute("""
        select id from ways_vertices_pgr, ST_GeomFromEWKT('SRID=4326;POINT({} {})') as pnt
        where ST_DWithin(ways_vertices_pgr.the_geom, pnt, 0.001)
        order by ST_Distance(ways_vertices_pgr.the_geom, pnt)
        limit 1
        """.format(lng, lat))

        r = cur.fetchone()[0]

        return r

    def get_route(self, start, end):
        cur = self.get_curr()

        # print("""
        # SELECT node, edge FROM pgr_dijkstra(
        #     'SELECT gid AS id,
        #         source,
        #         target,
        #         length AS cost
        #         FROM ways',
        #     {}, {},
        #     directed := false
        # );
        # """.format(start, end))

        cur.execute("""
        SELECT node, edge, agg_cost FROM pgr_dijkstra(
            'SELECT gid AS id,
                source,
                target,
                cost,
                reverse_cost
                FROM ways',
            {}, {},
            directed := true
        );
        """.format(start, end))

        r = cur.fetchall()

        return r

    def get_privacy_route(self, start, end):
        cur = self.get_curr()

        cur.execute("""
        SELECT node, edge, agg_cost FROM pgr_dijkstra(
            'SELECT gid AS id,
                source,
                target,
                cost + camera * 1000 AS cost,
                reverse_cost + camera * 1000 as reverse_cost,
                FROM ways',
            {}, {},
            directed := t   rue
        );
        """.format(start, end))

        return cur.fetchall()

    def route_to_geojson(self, route):
        # print(route)

        if len(route) == 0:
            return {
                "type": "FeatureCollection",
                "features": []
            }, 0, 0

        cur = self.get_curr()

        coordinates = []

        prev = -1
        length = 0.
        feature = None
        coordinates = None
        features = []

        total_length = 0
        gluur_length = 0

        def new_feature(cameras):
            return {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": None
                },
                "properties": {
                    "cameras": cameras
                }
            }

        for step in route:
            if step[1] > 0:
                cur.execute("""
                select ST_AsGeoJSON(the_geom), camera, length_m, source, target from ways where gid = {}
                """.format(step[1]))


                way = cur.fetchone()

                print(step[0], way[3], way[4])


                # Aantal camera's veranderd
                if way[1] != prev:
                    if feature is not None:
                        feature['geometry']['coordinates'] = coordinates
                        feature['properties']['lengte'] = length
                        features.append(feature)

                        total_length += length

                        if prev > 0:
                            gluur_length += length
                    
                    coordinates = []
                    feature = new_feature(way[1])
                    prev = way[1]
                    length = 0
                
                length += way[2]

                gj = loads(way[0])

                if (step[0] != way[3]):
                    new_coords = gj['coordinates'][::-1]
                else:
                    new_coords = gj['coordinates']

                if (len(coordinates) == 0):
                    coordinates.extend(new_coords)
                else:
                    coordinates.extend(new_coords[1:])

        if feature is not None:
            feature['geometry']['coordinates'] = coordinates
            feature['properties']['lengte'] = length
            features.append(feature)

            total_length += length

            if prev > 0:
                gluur_length += length
            

        return {
            'type': 'FeatureCollection',
            'features': features,
        }, total_length, gluur_length

    def intersect(self):
        pass
