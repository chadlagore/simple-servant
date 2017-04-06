import os, sys

proj_path = "/Users/chadlagore/git/simple_servant"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simple_servant.settings")
sys.path.append(proj_path)
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from traffic_api.models import IntersectionData

nw_bounds = (49.27754873849731,-123.24093818664551)
se_bounds = (49.26556423534828,-123.2197380065918)


def kill_rows(lon_min, lat_min, lon_max, lat_max):
    '''
    Applies a string of filters to a query before calling delete.

    '''
    objects = IntersectionData.objects.filter(
        latitude__gte=lat_min,
        latitude__lte=lat_max,
        longitude__gte=lon_min,
        longitude__lte=lon_max
    )

    print(str(len(objects)) + " objects found.")
    objects.delete()

    objects = IntersectionData.objects.filter(
        latitude__gte=lat_min,
        latitude__lte=lat_max,
        longitude__gte=lon_min,
        longitude__lte=lon_max
    )

    print(str(len(objects)) + " objects after deletion.")


def main():
    lat_min = min(nw_bounds[0], se_bounds[0])
    lat_max = max(nw_bounds[0], se_bounds[0])
    lon_min = min(nw_bounds[1], se_bounds[1])
    lon_max = max(nw_bounds[1], se_bounds[1])

    kill_rows(
        lon_min=lon_min,
        lat_min=lat_min,
        lon_max=lon_max,
        lat_max=lat_max
    )


if __name__ == '__main__':
    main()
