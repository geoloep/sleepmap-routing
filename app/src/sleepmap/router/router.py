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
        SELECT node, edge FROM pgr_dijkstra(
            'SELECT gid AS id,
                source,
                target,
                length AS cost
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
        SELECT node, edge FROM pgr_dijkstra(
            'SELECT gid AS id,
                source,
                target,
                cost + camera * 10000 AS cost
                FROM ways',
            {}, {},
            directed := true
        );
        """.format(start, end))

        return cur.fetchall()

    def route_to_geojson(self, route):
        cur = self.get_curr()

        coordinates = []

        for step in route:
            # print(step)

            if step[1] > 0:
                cur.execute("""
                select ST_AsGeoJSON(the_geom) from ways where gid = {}
                """.format(step[1]))

                gj = loads(cur.fetchone()[0])

                if (len(coordinates) == 0):
                    coordinates.extend(gj['coordinates'])
                else:
                    coordinates.extend(gj['coordinates'][1:])

        return {
            'type': 'LineString',
            'coordinates': coordinates,
        }

    def intersect(self):
        pass
