import psycopg2
from json import loads

conn = psycopg2.connect("host=postgresql dbname=routing user=postgres")
cur = conn.cursor()

cur.execute("""
update public.ways
set camera = 0
""")

conn.commit()

cur.execute("""
select st_astext(wkb_geometry) from viewsheds where ST_IsValid(wkb_geometry)
""")

for vs in cur.fetchall():
    q = """
    with ways as (
        select gid, the_geom from ways)
    select gid from ways where ST_Intersects(ways.the_geom, ST_GeomFromEWKT('SRID=4326;{}'))
    """.format(vs[0])


    cur.execute(q)

    for gids in cur.fetchall():
        print(gids)
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
        
