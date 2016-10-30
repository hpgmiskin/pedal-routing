import sys
import json
import datetime
import osmium

import database
import shape_tools
import shape_plotter

database = database.Database()
database.connect()

def replace_print(message):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(message)
    sys.stdout.flush()

class Counter(osmium.SimpleHandler):

    def __init__(self,filename):
        osmium.SimpleHandler.__init__(self)
        self.nodes = 0
        self.ways = 0
        self.relations = 0

        print('Counting')
        self.apply_file(filename)
        print('Found {} nodes, {} ways and {} relations'.format(self.nodes,self.ways,self.relations))

    def node(self, node):
        self.nodes += 1

    def way(self, way):
        self.ways += 1

    def relation(self, relation):
        self.relations += 1


class WayHandler(osmium.SimpleHandler):

    def __init__(self, idx, counter, writer, shape_tools=shape_tools.ShapeTools(), shape_plotter=shape_plotter.ShapePlotter()):
        osmium.SimpleHandler.__init__(self)
        self.idx = idx
        self.ways = 0
        self.counter = counter
        self.writer = writer
        self.shape_tools = shape_tools
        self.shape_plotter = shape_plotter


    def node(self, node):
        self.writer.add_node(node)

    def way(self, way):

        def way_name():
            if ('name' in way.tags):
                return way.tags['name']

        def way_collisions():
            if ('collisions' in way.tags):
                return way.tags['collisions']

        # print(way_name(),way_collisions())

        coordinates = []
        for node in way.nodes:
            loc = idx.get(node.ref)
            coordinates.append((loc.lat,loc.lon))

        line = self.shape_tools.create_line(coordinates)
        line_buffer_coordinates = self.shape_tools.get_line_buffer_coordinates(coordinates)

        query = dict(
            date__gte=datetime.date(2014, 1, 1),
            location__geo_within_polygon=line_buffer_coordinates,
            severity='Serious'
        )
        accidents = database.Accident.objects(**query)

        tags = [tag for tag in way.tags]
        tags.append(('collisions',str(accidents.count())))

        self.ways += 1
        percent = int(100 * self.ways / self.counter.ways)
        replace_print('{}/{} ways processed ({}%)'.format(self.ways,self.counter.ways,percent))
        self.writer.add_way(way.replace(tags=tags))

    def relation(self, relation):
        self.writer.add_relation(relation)

if (__name__ == "__main__"):

    input_file = 'data/greater-london-latest.osm.pbf'
    output_file = 'data/greater-london-collisions.osm.pbf'

    counter = Counter(input_file)

    idx = osmium.index.create_map('sparse_file_array,data/node-cache.nodecache')
    locations = osmium.NodeLocationsForWays(idx)
    locations.ignore_errors()

    writer = osmium.SimpleWriter(output_file)
    handler = WayHandler(idx,counter,writer)

    nodes = osmium.io.Reader(input_file, osmium.osm.osm_entity_bits.NODE)
    osmium.apply(nodes, locations)
    nodes.close()

    ways = osmium.io.Reader(input_file, osmium.osm.osm_entity_bits.WAY)
    osmium.apply(ways, locations, handler)
    ways.close()

    writer.close()
