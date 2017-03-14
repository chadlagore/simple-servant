'''
Pipeline:

'''
import time
import json
from OverpassClient import OverpassClient
from imposm.parser import OSMParser

in_file = 'vancouver_west'
outfile_city = in_file + '.json'
osm_file = in_file + '.osm'

# A mapping from names to refs.
names_to_refs = {}

# Nodes to cords.
nodes_to_coords = {}

# A nestedlist of all the intersections (nodes and street names).
intersections = []

# A list of just the nodes corresponding to the intersections.
nodes_we_want = []


class HighwayCallback(object):
    ''' Callback for a highway object. '''
    def ways(self, ways):
        for id_, tag, refs in ways:
            if 'name' in tag.keys() and 'highway' in tag.keys():
                if tag['highway'] != 'cycleway':
                    names_to_refs[tag['name']] = refs


def find_intersections(d):
    ''' Given a dict of lists, finds intersecting elements. '''
    for name_i, nodes_i in d.iteritems():
        for name_j, nodes_j in d.iteritems():
            if name_i != name_j:
                result = set(nodes_i).intersection(nodes_j)
                if result:
                    intersections.append((list(result), name_i, name_j))
                    nodes_we_want.extend(list(result))


def collect_ways():
    ''' Collects all ways from a local file. '''
    ways_callback = HighwayCallback()
    p = OSMParser(concurrency=4, ways_callback=ways_callback.ways)
    p.parse(osm_file)


def collect_nodes():
    ''' Collects all nodes from a local file. '''
    overpass = OverpassClient()
    i = 0
    n = len(intersections)
    for intersection in intersections:
        for node in intersection[0]:
            res = first(overpass.get_node(node)['elements'])
            nodes_to_coords[node] = (
                res['lat'], res['lon'], intersection[1], intersection[2]
            )
            i = i + 1
            print("{} of {} requests".format(i, n))


def first(l, condition=lambda x: True, default=None):
    return next((i for i in l if condition(i)), default)


def main():
    start = time.time()
    collect_ways()
    find_intersections(names_to_refs)
    collect_nodes()
    with open(outfile_city, 'w') as outfile:
        json.dump(nodes_to_coords, outfile, indent=4)
    end = time.time()
    print(end-start)


if __name__ == '__main__':
    main()
