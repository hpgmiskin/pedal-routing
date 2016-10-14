import sys
import json
import osmium

import shape_tools
import shape_plotter

class WayHandler(osmium.SimpleHandler):

    def __init__(self, idx, shape_tools=shape_tools.ShapeTools(), shape_plotter=shape_plotter.ShapePlotter()):
        osmium.SimpleHandler.__init__(self)
        self.idx = idx
        self.shape_tools = shape_tools
        self.shape_plotter = shape_plotter

    def way(self, way):
        if ('name' in way.tags): print(way.tags['name'])
        else: print('No name')

        coordinates = []
        for node in way.nodes:
            loc = idx.get(node.ref)
            coordinates.append((loc.lat,loc.lon))

        line = self.shape_tools.create_line(coordinates)
        line_buffer = self.shape_tools.create_line_buffer(coordinates)

        self.shape_plotter.plot_mappings([line,line_buffer])

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