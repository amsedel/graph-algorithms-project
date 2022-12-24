import numpy
import math


# Spring Class, Eades

class Spring:
    def __init__(self, g):
        self.c1 = 125
        self.c2 = 150
        self.graph = g

    def motion(self):

        for node in self.graph._Grafo__nodes.values():
            node.attrib['displacement'] = numpy.array([0, 0])

        for edge in self.graph._Grafo__edges:
            p_n0 = edge._Arista__pair[0].attrib['position']
            p_n1 = edge._Arista__pair[1].attrib['position']
            delta = p_n0 - p_n1
            euclidian_d = numpy.linalg.norm(delta)
            f_u = math.log10(euclidian_d/ self.c1) * self.c2 * delta/euclidian_d 
            #opposing forces in the spring
            edge._Arista__pair[0].attrib['displacement'] = edge._Arista__pair[0].attrib['displacement'] + f_u
            edge._Arista__pair[1].attrib['displacement'] = edge._Arista__pair[1].attrib['displacement'] - f_u

        for node in self.graph._Grafo__nodes.values():
            #update positions
            node.attrib['position'] = node.attrib['position'] + node.attrib['displacement']

