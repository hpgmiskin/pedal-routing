import os
import sys
import json
import shutil
import datetime
import osmium

import timer
import database
import shape_tools
import shape_plotter

timer = timer.Timer()
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
        print('Add node')
        self.writer.add_node(node)

    def way(self, way):


        way_name = None
        if ('name' in way.tags):
            way_name = way.tags['name']

        def way_collisions():
            if ('collisions' in way.tags):
                return way.tags['collisions']

        # If collisions found add ways
        if ('collisions' in way.tags):
            return self.writer.add_way(way)

        coordinates = []
        for node in way.nodes:
            loc = idx.get(node.ref)
            coordinates.append((loc.lat,loc.lon))

        if (self.ways < 10000):
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
            way = way.replace(tags=tags)

        self.ways += 1
        percent = int(100 * self.ways / self.counter.ways)
        # replace_print('{}/{} ways processed ({}%)'.format(self.ways,self.counter.ways,percent))

        self.writer.add_way(way)

    def relation(self, relation):
        self.writer.add_relation(relation)

if (__name__ == "__main__"):

    original_file = 'data/greater-london-latest.osm.pbf'
    collisions_file = 'data/greater-london-collisions.osm.pbf'

    input_file = 'data/greater-london-input.osm.pbf'
    output_file = 'data/greater-london-output.osm.pbf'

    shutil.copyfile(original_file,input_file)
    counter = Counter(input_file)
    
    idx = osmium.index.create_map('sparse_file_array,data/node-cache.nodecache')
    locations = osmium.NodeLocationsForWays(idx)
    locations.ignore_errors()

    nodes = osmium.io.Reader(input_file, osmium.osm.osm_entity_bits.NODE)
    osmium.apply(nodes, locations)
    nodes.close()

    while True:

        timer.start()

        try:
            print('Remove output file')
            os.remove(output_file)
        except OSError as error:
            print(error)

        writer = osmium.SimpleWriter(output_file)
        handler = WayHandler(idx,counter,writer)
        ways = osmium.io.Reader(input_file, osmium.osm.osm_entity_bits.WAY)
        osmium.apply(ways, locations, handler)
        ways.close()
        writer.close()

        timer.stop()
        print('Scanned 10000 ways in {}'.format(timer.duration))

        # If no ways have been altered then break loop
        if (not handler.ways):
            print('Break Loop')
            break

        # Copy output file
        shutil.copyfile(output_file,input_file)

    # Copy final file
    shutil.copyfile(output_file,collisions_file)
