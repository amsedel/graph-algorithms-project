import pygame
from constants import *
import math
import numpy as np

class Point:
    def __init__(self, x, y, data={}):
        self.x = x
        self.y = y
        self.data = data
    
    def distanceToCenter(self, center):
        return math.sqrt((center.x - self.x)**2 + (center.y - self.y)**2)

class Rectangle:
    #center is a point
    def __init__(self, center, width, height):
        self.center = center
        self.w = width
        self.h = height
        self.west = center.x - width
        self.east = center.x + width
        self.north = center.y - height
        self.south = center.y + height

    def containsPoint(self, point):
        return (self.west <= point.x < self.east) and (self.north <= point.y < self.south)

    #range it is a rectangle
    def intersects(self, range):
        return not (range.west > self.east or range.east < self.west or range.north > self.south or range.south < self.north)


    def draw(self, screen, color=WHITE):
        pygame.draw.rect(screen, color, (self.center.x-self.w, self.center.y - self.h,self.w*2, self.h*2), 1)


class QuadTree:
    # boundary is a rectangle
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.points = [] #points inside quadtree
        self.is_divided = False
        self.attrib = {
            'mass': 0,
            'pos_center_mass': np.zeros(2),
            'center_mass': np.zeros(2)
        }

    def insert(self, point):
        #verify if the point is in the range of current quadtree
        if not self.boundary.containsPoint(point):
            return False

        #if it has not reached capacity
        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.is_divided:
            self.divide()

        if self.nw.insert(point):
            return True
        elif self.ne.insert(point):
            return True
        elif self.sw.insert(point):
            return True
        elif self.se.insert(point):
            return True

        return False


    def divide(self):
        center_x = self.boundary.center.x
        center_y = self.boundary.center.y
        new_width = self.boundary.w / 2
        new_height = self.boundary.h / 2
        nw = Rectangle(Point(center_x - new_width, center_y - new_height), new_width, new_height)
        self.nw = QuadTree(nw)
        ne = Rectangle(Point(center_x + new_width, center_y - new_height), new_width, new_height)
        self.ne = QuadTree(ne)
        sw = Rectangle(Point(center_x - new_width, center_y + new_height), new_width, new_height)
        self.sw = QuadTree(sw)
        se = Rectangle(Point(center_x + new_width, center_y + new_height), new_width, new_height)
        self.se = QuadTree(se)

        self.is_divided = True


    def queryRange(self, range):
        found_points = []
        if not self.boundary.intersects(range):
            return []

        for point in self.points:
            if range.containsPoint(point):
                found_points.append(point)

        if self.is_divided:
            found_points.extend(self.nw.queryRange(range))
            found_points.extend(self.ne.queryRange(range))
            found_points.extend(self.sw.queryRange(range))
            found_points.extend(self.se.queryRange(range))

        return found_points
    

    def queryRadius(self,range, center):
        found_points = []
        if not self.boundary.intersects(range):
            return []

        for point in self.points:
            if range.containsPoint(point) and point.distanceToCenter(center) <= range.w:
                found_points.append(point)

        if self.is_divided:
            found_points.extend(self.nw.queryRadius(range, center))
            found_points.extend(self.ne.queryRadius(range, center))
            found_points.extend(self.sw.queryRadius(range, center))
            found_points.extend(self.se.queryRadius(range, center))

        return found_points
        

    def __len__(self):
        count = len(self.points)
        if self.is_divided == True:
            count += len(self.nw) + len(self.ne) + len(self.sw) + len(self.se)
        return count
    

    def draw(self, ax):
        self.boundary.draw(ax)
        if self.is_divided:
            self.nw.draw(ax)
            self.ne.draw(ax)
            self.sw.draw(ax)
            self.se.draw(ax)