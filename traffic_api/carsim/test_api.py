import requests


class StreetSmartClient:
    ''' A simple street smart client. '''

    base_url = "http://127.0.0.1:8000/"


    def __init__(self):
        pass


    def get_intersections_filter(self, **kwargs):
        print(kwargs)
        response = requests.get(
            self.base_url + 'traffic/intersections', kwargs)
        response.raise_for_status()
        return response.json()


data = dict(
    lat_gte=49.25,
    lat_lte=49.27,
    lon_lte=-123.10,
    lon_gte=-123.15
)

client = StreetSmartClient()
result = client.get_intersections_filter(**data)
print(len(result))
