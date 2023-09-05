from shapely import Polygon, Point
from Algorithms.Genetic.genetic_classes import Population, Being, Circle

polygon = Polygon([Point(0, 0), Point(20, 0), Point(60, 20), Point(10, 50), Point(-10, 40)])
population = Population(polygon, 10)

centers = [Point(-4.29032036, 40.83137302),
Point(27.19068503,  8.51072084),
Point(34.28243996, 10.34338072),
Point(25.40244838, 17.86065501),
Point(50.70503847, 20.50868517),
Point(33.62483318, 30.10323356),
Point(45.51086207, 26.16400947),
Point(10.01153288,  9.24643352),
Point(12.01946898,  4.09302518),
Point(28.79166789, 30.63710233)]

being = Being.from_circles(
    polygon,
    [Circle(c, 1) for c in centers])

cells = population._get_voronoi_polygons(being)