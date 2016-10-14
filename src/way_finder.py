import sys
import json
import osmium
import osmium.geom

import shapely.speedups
if shapely.speedups.available:
    shapely.speedups.enable()

import shapely.wkb

class WayHandler(osmium.SimpleHandler):

    def __init__(self, idx, geom_factory=osmium.geom.WKBFactory()):
        osmium.SimpleHandler.__init__(self)
        self.idx = idx
        self.geom_factory = geom_factory

    def way(self, way):
        if ('name' in way.tags): print(way.tags['name'])
        else: print('No name')

        linestring = self.geom_factory.create_linestring(way)
        print(linestring)

        linestring = shapely.wkb.loads(linestring, hex=True)
        print(linestring)
        print(dir(linestring))

        sys.exit()

        for node in way.nodes:
            loc = idx.get(node.ref)
            print('\t',loc.lat,loc.lon)


if (__name__ == "__main__"):

    idx = osmium.index.create_map('sparse_file_array,data/node-cache.nodecache')
    locations = osmium.NodeLocationsForWays(idx)
    locations.ignore_errors()

    nodes = osmium.io.Reader('data/greater-london-latest.osm.pbf', osmium.osm.osm_entity_bits.NODE)
    osmium.apply(nodes, locations)
    nodes.close()

    ways = osmium.io.Reader('data/greater-london-latest.osm.pbf', osmium.osm.osm_entity_bits.WAY)
    osmium.apply(ways, locations, WayHandler(idx))
    ways.close()