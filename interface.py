
import pygame
import numpy
import math
from constants import *

class Canvas:
    def __init__(self, graph) -> None:
        self.execution = True
        self.graph = graph
        self.size = SIZE


    def show(self):
        pygame.init()
        screen = pygame.display.set_mode(SIZE) #create window
        #clock to control animation in FPS
        clock = pygame.time.Clock()

        #create main loop
        while self.execution:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.execution = False
            screen.fill(BLACK) #paint background

            self.graph.draw(screen)
        
            pygame.display.flip() #update screen
            clock.tick(60)
        pygame.quit()


class Scale:
    def __init__(self, graph) -> None:
        self.graph = graph
        self.xy_scale = 1
        self.canvas_dims = numpy.array([[MARGIN,MARGIN],[SIZE[0]-MARGIN,SIZE[1]-MARGIN]])

    def calculate_graph_dims(self):
        xmin, ymin, xmax, ymax, x, y= math.inf,math.inf,0,0,0,0
        for i, node in enumerate(self.graph._Grafo__nodes.values()):
            if i == 0:
                x = node.attrib['position'][0]
                y = node.attrib['position'][1]
            else:
                if x >= node.attrib['position'][0]:
                    if x > xmax:
                        xmax = x
                    if xmin > node.attrib['position'][0]:
                        xmin = node.attrib['position'][0]
                if x < node.attrib['position'][0]:
                    if xmax < node.attrib['position'][0]:
                        xmax = node.attrib['position'][0]
                    if xmin > x:
                        xmin = x
                if y >= node.attrib['position'][1]:
                    if y > ymax:
                        ymax = y
                    if ymin > node.attrib['position'][1]:
                        ymin = node.attrib['position'][1]
                if y < node.attrib['position'][1]:
                    if ymax < node.attrib['position'][1]:
                        ymax = node.attrib['position'][1]
                    if ymin > y:
                        ymin = y
        return numpy.array([[xmin,ymin],[xmax,ymax]])


    def calculate_scale(self):
        self.graph_dims = self.calculate_graph_dims()
        self.graph_size = self.graph_dims[1] - self.graph_dims[0]
        self.canvas_size = self.canvas_dims[1]-self.canvas_dims[0]
        #Calculate scales
        x_scale = self.canvas_size[0] / self.graph_size[0]
        y_scale = self.canvas_size[1] / self.graph_size[1]
        if y_scale > x_scale:
            displacement = [0, ((y_scale - x_scale) / (y_scale * 2)) * self.canvas_size[1]]
            self.xy_scale = x_scale
        else: 
            displacement = [((x_scale - y_scale) / (x_scale * 2)) * self.canvas_size[0], 0]
            self.xy_scale = y_scale
        self.gap = numpy.array(displacement)

    def scaling(self, node_pos):
        return  self.canvas_dims[0] + self.gap + (self.xy_scale * (node_pos-self.graph_dims[0]))