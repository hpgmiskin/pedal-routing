import osmium.geom

import shapely.speedups
if shapely.speedups.available:
    shapely.speedups.enable()

import shapely.wkb
import shapely.geometry

import geom_tools


class ShapeTools:

    def __init__(self, geom_factory=osmium.geom.WKBFactory(), geom_tools=geom_tools.GeomTools()):
        self.geom_factory = geom_factory
        self.geom_tools = geom_tools

    def create_line(self,coordinates):
        """Crate a linestring from a list of nodes"""

        line = shapely.geometry.LineString(coordinates)
        return shapely.geometry.mapping(line)

    def create_line_buffer(self,coordinates,offset=10):
        """Find a buffer of a given line """

        # Take first point as reference
        reference = coordinates[0]

        # Find meter offsets from reference
        offsets = self.geom_tools.convert_coordinates_to_offsets(reference,coordinates)

        # Find the meter line 
        line = shapely.geometry.LineString(offsets)
        line_buffer = line.buffer(offset)

        line_buffer = shapely.geometry.mapping(line_buffer)
        # print(len(line_buffer['coordinates']))

        line_buffer_coordinates = []
        for section in line_buffer['coordinates']:
            for coordinate in section:
                line_buffer_coordinates.append(coordinate)

        # Find coordinates of line buffer
        coordinates = self.geom_tools.convert_offsets_to_coordinates(reference,line_buffer_coordinates)

        return self.create_line(coordinates)