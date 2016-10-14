import sys
import json
import datetime
import osmium

import database
import shape_tools
import shape_plotter

database = database.Database()
database.connect()

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
        line_buffer_coordinates = self.shape_tools.get_line_buffer_coordinates(coordinates)

        query = dict(
            location__geo_within_polygon=line_buffer_coordinates,
            severity='Serious'
        )
        accidents = database.Accident.objects(**query)

        if (accidents.count()):
            print('{} accidents found'.format(accidents.count()))
            line['label'] = 'Way'

            line_buffer = self.shape_tools.create_line(line_buffer_coordinates)
            line_buffer['label'] = 'Buffer'

            accident_locations = {
                'label':'Accidents',
                'coordinates':[ accident.location['coordinates'] for accident in accidents ]
            }
            self.shape_plotter.plot_mappings([line,line_buffer,accident_locations])

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