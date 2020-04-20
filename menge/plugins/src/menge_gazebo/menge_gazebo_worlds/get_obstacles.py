import rospy
import rospkg
import yaml

import numpy as np

from lxml import etree
from lxml.etree import Element


class ObstaclesSearcher(object):
    def __init__(self, filename):
        rospack = rospkg.RosPack()
        self.wolrd_path = rospack.get_path("menge_gazebo_worlds") 
        parser = etree.XMLParser(remove_blank_text=True)
        self.tree = etree.parse(self.wolrd_path + "/worlds/" + filename, parser)

        self.obstacles_size = dict()
        self.obstacles_pose = dict()

        self._get_size()
        self._get_pose()

    def _get_size(self):
        for i, link in enumerate(self.tree.getroot().getchildren()[0][9]):
            if i == 0 or i == len(self.tree.getroot().getchildren()[0][9]) - 1:
                continue
            # print "name: ", link.get("name")
            self.obstacles_size[link.get("name")] = np.asarray(link[0][0][0][0].text.split())
            # print link[0][0][0][0].tag, ":", link[0][0][0][0].text
            # print ""

    def _get_pose(self):
        for i, link in enumerate(self.tree.getroot().getchildren()[0][10][4]):
            if i < 2:
                continue
            # print "name: ", link.get("name")
            self.obstacles_pose[link.get("name")] = np.asarray(link[0].text.split())
            # print link[0].tag, ":", link[0].text
            # print ""

    def run(self):
        for i in self.obstacles_pose:
            print (self.obstacles_pose[i]), self.obstacles_size[i]
            # print "Wall_" + str(i)
            # print self.obstacles_size["Wall_" + str(i)]
            # print self.obstacles_pose["Wall_" + str(i)]
            print ""
        

if __name__ == "__main__":
    searcher = ObstaclesSearcher("corridor1.world")
    searcher.run()