import sys
import json
import osmium
import osmium.geom

import shapely.speedups
if shapely.speedups.available:
    shapely.speedups.enable()

import shapely.wkb
import shapely.geometry

import geom_tools

class WayHandler(osmium.SimpleHandler):

    def __init__(self, idx, geom_factory=osmium.geom.WKBFactory(), geom_tools=geom_tools.GeomTools()):
        osmium.SimpleHandler.__init__(self)
        self.idx = idx
        self.geom_factory = geom_factory
        self.geom_tools = geom_tools

    def way(self, way):
        if ('name' in way.tags): print(way.tags['name'])
        else: print('No name')

        linestring = self.geom_factory.create_linestring(way.nodes)
        lat_lng_line = shapely.wkb.loads(linestring, hex=True)

        # line_coordinates = shapely.geometry.mapping(line)
        reference = lat_lng_line.bounds[:2]
        print('reference',reference)
        coordinates = lat_lng_line.coords[:]
        print('coordinates',coordinates)

        # Find meter offsets
        offsets = self.geom_tools.convert_coordinates_to_offsets(reference,coordinates)
        meter_line = shapely.geometry.LineString(offsets)
        meter_line_buffer = meter_line.buffer(10)

        data = [
            shapely.geometry.mapping(meter_line),
            shapely.geometry.mapping(meter_line_buffer)
        ]

        print(data)

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