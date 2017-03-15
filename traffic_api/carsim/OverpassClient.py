import requests


class OverpassClient(object):

    ''' A simple overpass-api.de client. '''

    base_url = 'http://overpass-api.de/api/'
    way_endpoint = 'interpreter?data=[out:json];way({});(._;>;);out;'
    node_endpoint = 'interpreter?data=[out:json];node({});(._;>;);out;'
    streets_list = 'area[name="{}"];way(area)[highway][name];out;'

    def __init__(self):
        pass

    def get_way(self, way):
        try:
            req = self.base_url + self.way_endpoint.format(way)
            return requests.get(req).json()
        except:
            print('Request for way failed.')
            return None


    def get_node(self, node):
        try:
            req = self.base_url + self.node_endpoint.format(node)
            return requests.get(req).json()
        except:
            print('Request for node failed.')
            return None
