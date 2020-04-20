import tf
import rospkg

import numpy as np

from lxml import etree
from lxml.etree import Element
from get_obstacles import ObstaclesSearcher

class ObstaclesWriter(object):
    def __init__(self, filename):
        rospack = rospkg.RosPack()
        self.world_path = rospack.get_path("menge_gazebo_worlds")
        parser = etree.XMLParser(remove_blank_text=True)
        self.tree = etree.parse(self.world_path + "/" + filename, parser)

        self.searcher = ObstaclesSearcher("corridor1.world")
        self.file = open("input.txt", 'w')
        self.img_width = 1538
        self.img_high = 383

    def _world_to_pixel(self, point):
        pixel_point = np.zeros(2)
        pixel_point[0] = (point[0][0] / 0.05) + 767
        pixel_point[1] = -(point[1][0] / 0.05) + 238
        return pixel_point

    def run(self):
        experiment = self.tree.getroot()
        obstacle_set = Element("ObstacleSet", type="explicit", abcdef="1")
        
        for i in self.searcher.obstacles_pose:
            x = float(self.searcher.obstacles_pose[i][0])
            y = float(self.searcher.obstacles_pose[i][1])
            length = float(self.searcher.obstacles_size[i][0])
            width = float(self.searcher.obstacles_size[i][1])
            yaw = float(self.searcher.obstacles_pose[i][5])
            # yaw = np.pi / 2.
            R = tf.transformations.rotation_matrix(yaw, (0, 0, 1))
            T = tf.transformations.translation_matrix((x, y, 0))
            print "x: ", x, " y: ", y, " yaw: ", yaw, " length: ", length, " width: ", width
            print " ------- "
            print R
            print T
            # T = np.dot(-R, T)
            # R = np.asarray(np.mat(R).I)
        

            
            points = []
            points.append(np.array([[-length / 2.], [-width / 2.], [0.], [1.0]]))
            points.append(np.array([[-length / 2.], [width / 2.], [0.], [1.0]]))
            points.append(np.array([[length / 2.], [width / 2.], [0.], [1.0]]))
            points.append(np.array([[length / 2.], [-width / 2.], [0.], [1.0]]))

            obstacle = Element("Obstacle", closed="1")
            world_points = []
            for j, point in enumerate(points):
                point = (np.dot(T, np.dot(R, point))[0:2])
                vertex = Element("Vertex", p_x=str(point[0][0]), p_y=str(point[1][0]))
                obstacle.append(vertex)
                world_points.append(self._world_to_pixel(point))
                
            point_str = "(%d, %d), (%d, %d), (%d, %d), (%d, %d)\n"
            point_str = point_str % (world_points[0][0], world_points[0][1],\
                                     world_points[1][0], world_points[1][1],\
                                     world_points[2][0], world_points[2][1],\
                                     world_points[3][0], world_points[3][1])  
            self.file.write(point_str)
            obstacle_set.append(obstacle)
            
        
        experiment.append(obstacle_set)

        self.tree.write(self.world_path + '/test.xml', pretty_print=True, xml_declaration=True, encoding="utf-8")


if __name__ == "__main__":
    writer = ObstaclesWriter("circleS.xml")
    writer.run()
