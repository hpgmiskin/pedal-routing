import matplotlib.pyplot

class ShapePlotter:

    def __init__(self,plot=matplotlib.pyplot):
        self.plot = plot

    def plot_mappings(self,data):

        colors = ['red', 'green', 'blue']

        for index,series in enumerate(data):
            label = series.get('label')
            color = colors[index % len(colors)]

            coordinates = series['coordinates']

            def plot(coordinates):
                xs = [coordinate[0] for coordinate in coordinates]
                ys = [coordinate[1] for coordinate in coordinates]
                self.plot.scatter(xs, ys, c=color, label=label, alpha=0.3, edgecolors='none')

            if (type(coordinates[0]) is float):
                plot([coordinates])
            elif (type(coordinates[0][0]) is float):
                plot(coordinates)
            elif (type(coordinates[0][0][0]) is float):
                [plot(coords) for coords in coordinates]


        self.plot.legend()
        self.plot.show()

if (__name__ == '__main__'):

    shape_plotter = ShapePlotter()
    shape_plotter.plot_mappings([{'coordinates': ((0.0, 0.0), (13.40280202629316, 14.605117192077268)), 'type': 'LineString'}])