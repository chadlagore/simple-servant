import psycopg2
import os

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()

nw_bounds = (49.257330202816156,-123.23136806488037)
se_bounds = (49.238896675301426,-123.20188522338867)


def kill_rows(filters):
    '''
    Applies a string of filters to a query before calling delete.

    '''
    filter_string = ' and '.join(filters)
    query = "DELETE FROM traffic_api_intersectiondata WHERE %s;"
    cur.execute(query, (filter_string, ))
    cur.commit()


def main():
    lat_min = min(nw_bounds[0], se_bounds[0])
    lat_max = max(nw_bounds[0], se_bounds[0])
    lon_min = min(nw_bounds[1], se_bounds[1])
    lon_max = max(nw_bounds[1], se_bounds[1])

    kill_rows(
        filters=(
            'latitude > {}'.format(lat_min),
            'latitude < {}'.format(lat_max),
            'longitude > {}'.format(lon_min),
            'longitude < {}'.format(lon_max)
        )
     )


if __name__ == '__main__':
    main()
