import math

class GeomTools:

    R = 6378137

    def calculate_offset(self,coordinate_a,coordinate_b):
        """Find the horizontal and vertical offset between coordinates
        """

        [lat_a,lng_a] = coordinate_a
        [lat_b,lng_b] = coordinate_b

        x = math.pi * self.R * (lng_b - lng_a) * math.cos( math.pi * lat_a / 180 ) / 180
        y = math.pi * self.R * (lat_b - lat_a) / 180

        return [x,y]


    def calculate_coordinate(self,coordinate,offset):
        """Find the coordinate offset by given amount from coordinate
        """

        [lat_a,lng_a] = coordinate
        [x,y] = offset

        lat_b = lat_a + 180 * y / ( math.pi * self.R )
        lng_b = lng_a + 180 * x / ( math.pi * self.R * math.cos( math.pi * lat_a / 180 ) )

        return [lat_b,lng_b]



if (__name__ == "__main__"):

    geom_tools = GeomTools()
    offset = geom_tools.calculate_offset((41.49008, -71.312796),(41.499498, -81.695391))
    print(offset,math.sqrt(offset[0]**2+offset[1]**2))
    coordinate = geom_tools.calculate_coordinate((41.49008, -71.312796),offset)
    print(coordinate)
