import numpy as np
import math
from constants import *
from quadtree import Point, Rectangle, QuadTree
import pygame


# Spring Class, Eades

class Spring:
    def __init__(self, g, c=2):
        self.c1 = c
        self.c2 = c / 2
        self.graph = g
        self.k = c * 2

    def calculate_motion(self):
        
        #calculate repulsive force
        for v in self.graph._Grafo__nodes.values():
            # initialize displacement vector 
            v.attrib['displacement'] = np.array([0, 0])
            for u in self.graph._Grafo__nodes.values():
                if u != v:
                    # distance between u and v
                    delta = v.attrib['position'] - u.attrib['position']
                    dist = np.linalg.norm(delta) #euclidian distance
                    f_rep = (self.k**2) / dist
                    v.attrib['displacement'] = v.attrib['displacement'] + ((delta/dist) * f_rep)

        for edge in self.graph._Grafo__edges:
            pos_v = edge._Arista__pair[0].attrib['position']
            pos_u = edge._Arista__pair[1].attrib['position']
            delta_e = pos_v - pos_u
            dist_e = np.linalg.norm(delta_e) #euclidian distance
            #f_attr = (dist_e**2) / self.k
            f_attr = math.log10(dist/self.c2)*self.c1
            edge._Arista__pair[0].attrib['displacement'] = edge._Arista__pair[0].attrib['displacement'] - ((delta_e/dist_e) * f_attr)
            edge._Arista__pair[1].attrib['displacement'] = edge._Arista__pair[1].attrib['displacement'] + ((delta_e/dist_e) * f_attr)

        #update positions
        for node in self.graph._Grafo__nodes.values():
            d_desp = np.linalg.norm(node.attrib['displacement'])
            node.attrib['position'] = node.attrib['position'] + (node.attrib['displacement']/d_desp)



# Fruchterman Reigold Class
class Fruchterman_Reigold:
    def __init__(self, g, alpha=15, boundary = 0.001, num_convergences=15):
    # param: g, Graph
    # param: alpha, control convergence speed
    # param: boundary, difference tolerance between displacements
    # param: num_convergences, number of consecutive convergences according to the established boundary
        self.graph = g
        self.W = SIZE[0]-(MARGIN*2)
        self.H = SIZE[1]-(MARGIN*2)
        self.area = self.W * self.H
        self.alpha = alpha
        self.k = round(math.sqrt(self.area / len(self.graph._Grafo__nodes.keys())),3) #optimal distance
        self.iterations = 0
        self.t = self.alpha * len(self.graph._Grafo__nodes.keys()) #time
        self.has_converged = False 
        self.displacement_boundary = boundary * len(self.graph._Grafo__nodes.keys())
        self.displacement_delta = 0
        self.count = []
        self.num_consecutive_convergences = num_convergences

    def cooling(self):
        dt=self.t/float(self.iterations+1)
        self.t = self.t - dt

    def calculate_motion(self):

        if self.has_converged:
            #print("converged")
            return

        #print("iterations", self.iterations)
        
        #compute repulsive force
        for v in self.graph._Grafo__nodes.values():
            # initialize displacement vector 
            v.attrib['displacement'] = np.array([0, 0])
            for u in self.graph._Grafo__nodes.values():
                if u != v:
                    # distance between u and v
                    delta = v.attrib['position'] - u.attrib['position']
                    dist = np.linalg.norm(delta) #euclidian distance
                    f_rep = (self.k**2) / dist
                    v.attrib['displacement'] = v.attrib['displacement'] + ((delta/dist) * f_rep)

        #compute attractive force
        for edge in self.graph._Grafo__edges:
            pos_v = edge._Arista__pair[0].attrib['position']
            pos_u = edge._Arista__pair[1].attrib['position']
            delta_e = pos_v - pos_u
            dist_e = np.linalg.norm(delta_e) #euclidian distance
            f_attr = (dist_e**2) / self.k
            edge._Arista__pair[0].attrib['displacement'] = edge._Arista__pair[0].attrib['displacement'] - ((delta_e/dist_e) * f_attr)
            edge._Arista__pair[1].attrib['displacement'] = edge._Arista__pair[1].attrib['displacement'] + ((delta_e/dist_e) * f_attr)


        #update positions
        disp_delta = np.zeros(2)
        for node in self.graph._Grafo__nodes.values():
            d_desp = np.linalg.norm(node.attrib['displacement'])
            disp_delta = disp_delta + (node.attrib['displacement'] / d_desp)
            node.attrib['position'] = node.attrib['position'] + (node.attrib['displacement']/d_desp) * min(d_desp,self.t)

        self.iterations = self.iterations + 1
        self.cooling()

        _disp_delta = np.linalg.norm(disp_delta)
        displacement = _disp_delta - self.displacement_delta

        if self.displacement_boundary > displacement:
            self.count.append(displacement)
        else:
            self.count = []

        self.displacement_delta = _disp_delta

        # control convergence
        if len(self.count) >= self.num_consecutive_convergences:
            self.has_converged = True


# Barnes Hut Class
class Barnes_Hut:
    def __init__(self, g, capacity=6, theta=1, alpha=15, boundary = 0.00005, num_convergences=50):
    # param: g, Graph
    # param: capacity, maximun number of points in a quadtree
    # param: alpha, decide is a point is far enough from the center of mass of a group of points
    # param: alpha, control convergence speed
    # param: boundary, difference tolerance between displacements
    # param: num_convergences, number of consecutive convergences according to the established boundary
        self.graph = g
        self.capacity = self.calculate_capacity(capacity)
        self.theta = theta
        self.W = SIZE[0]-(MARGIN*2)
        self.H = SIZE[1]-(MARGIN*2)
        self.area = self.W * self.H
        self.alpha = alpha #control convergence speed
        self.k = round(math.sqrt(self.area / len(self.graph._Grafo__nodes.keys())),3) #optimal distance
        self.iterations = 0
        self.t = self.alpha * len(self.graph._Grafo__nodes.keys()) #time
        self.has_converged = False 
        self.displacement_boundary = boundary * len(self.graph._Grafo__nodes.keys())
        self.displacement_delta = 0
        self.count = []
        self.num_consecutive_convergences = num_convergences


    def calculate_capacity(self, capacity):
        len_nodes = len(self.graph._Grafo__nodes.keys())
        if len_nodes > 100:
            return int(capacity * (len_nodes / 100))
        else:
            return int(capacity)


    def create_quadtree(self):
        #graph_domain = self.graph.get_domain_graph()
        #w = (graph_domain[1][0] - graph_domain[0][0]) / 2
        #h = (graph_domain[1][1] - graph_domain[0][1]) / 2
        #domain = Rectangle(Point(w + graph_domain[0][0],h + graph_domain[0][1]), w, h)
        domain = Rectangle(Point(SIZE[0]/2,SIZE[1]/2), (SIZE[0]-MARGIN*2)/2, (SIZE[1]-MARGIN*2)/2)
        self.quadtree = QuadTree(domain, self.capacity)
        points = []
        for node in self.graph._Grafo__nodes.values():
            point = Point(node.attrib['position'][0], node.attrib['position'][1], node)
            points.append(point)
            self.quadtree.insert(point)
        #print("Total points: ", len(self.quadtree))
        #self.draw_quadtree(points)


    def calculate_massAndCenterOfMass(self, quadtree):
        # Center of mass:
        # x = x_1*m_1 + x_2*m_2 + ... + x_n*m_n / m_1 + m_2 + ... + m_n
        # y = y_1*m_1 + y_2*m_2 + ... + y_n*m_n / m_1 + m_2 + ... + m_n
        # Consider mass value = 1, therefore it is unnecessary to multiply the mass by the position
        
        for point in quadtree.points:
            quadtree.attrib['mass'] += 1 # mass value is 1
            quadtree.attrib['pos_center_mass'] += np.array([point.x, point.y])

        if quadtree.is_divided:
            #execute recursivity 
            self.calculate_massAndCenterOfMass(quadtree.nw)
            self.calculate_massAndCenterOfMass(quadtree.ne)
            self.calculate_massAndCenterOfMass(quadtree.sw)
            self.calculate_massAndCenterOfMass(quadtree.se)

            if len(quadtree.nw.points) > 0:
                quadtree.attrib['mass'] += quadtree.nw.attrib['mass']
                quadtree.attrib['pos_center_mass'] += quadtree.nw.attrib['pos_center_mass']

            if len(quadtree.ne.points) > 0:
                quadtree.attrib['mass'] += quadtree.ne.attrib['mass']
                quadtree.attrib['pos_center_mass'] += quadtree.ne.attrib['pos_center_mass']
            
            if len(quadtree.sw.points) > 0:
                quadtree.attrib['mass'] += quadtree.sw.attrib['mass']
                quadtree.attrib['pos_center_mass'] += quadtree.sw.attrib['pos_center_mass']
            
            if len(quadtree.se.points) > 0:
                quadtree.attrib['mass'] += quadtree.se.attrib['mass']
                quadtree.attrib['pos_center_mass'] += quadtree.se.attrib['pos_center_mass']

        if len(quadtree.points) > 0:
            quadtree.attrib['center_mass'] = quadtree.attrib['pos_center_mass'] / quadtree.attrib['mass']


    def draw_quadtree(self, points):
        #first execute create_quadtree()
        pygame.init()
        screen = pygame.display.set_mode((SIZE)) #create window
        #clock to control animation in FPS
        clock = pygame.time.Clock()
        execution = True
        #create main loop
        while execution:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    execution = False
            screen.fill(BLACK) #paint background
            for p in points:
                pygame.draw.circle(screen, BLUE, (p.x,p.y),4)
            self.quadtree.draw(screen)
            pygame.display.flip() #update screen
            clock.tick(60)
        pygame.quit()


    def F_rep_with_BarnesHut(self, point, quadtree):
        #Barnes Hut Algorithm:
        s = min(quadtree.boundary.w, quadtree.boundary.h)
        delta = point.data.attrib['position'] - quadtree.attrib['center_mass']
        d = np.linalg.norm(delta) # euclidian distance
        f_rep = np.zeros(2)

        if d == 0: #avoid division by zero
            return f_rep
        # 1) If the current node it is an external node (it not has children or the 
        # quadtree is not divided) and not is the same node, calculate the force and add it
        # 2) Otherwise, calculate the ratio s/d. If s/d < θ, treat this internal node (node with children) 
        #as a single body, and calculate the force it exerts on body b, and add it:
            # s is the width or height of the region represented by the internal node
            # d is the distance between the body and the node’s center-of-mass.
            # If s / d < θ, then the internal node is sufficiently far away
        if quadtree.is_divided == False or s/d < self.theta:
            f_rep = f_rep + ((self.k**2) / d) * quadtree.attrib['mass']
            return f_rep
        # 3) Otherwise, run the procedure recursively on each of the current node’s children
        else:
            f_rep = f_rep + self.F_rep_with_BarnesHut(point, quadtree.nw)
            f_rep = f_rep + self.F_rep_with_BarnesHut(point, quadtree.ne)
            f_rep = f_rep + self.F_rep_with_BarnesHut(point, quadtree.sw)
            f_rep = f_rep + self.F_rep_with_BarnesHut(point, quadtree.se)
            return f_rep


    def cooling(self):
        dt=self.t/float(self.iterations+1)
        self.t = self.t - dt


    def calculate_motion(self):

        if self.has_converged:
            #print("converged")
            return
        #print("iterations", self.iterations)
        
        #calculate repulsive force
        self.create_quadtree()
        self.calculate_massAndCenterOfMass(self.quadtree)
        for node in self.graph._Grafo__nodes.values(): 
            node.attrib['displacement'] = np.array([0, 0])
            point = Point(node.attrib['position'][0], node.attrib['position'][1], node)
            node.attrib['displacement'] = node.attrib['displacement'] + self.F_rep_with_BarnesHut(point, self.quadtree)
        
        #calculate attractive force
        for edge in self.graph._Grafo__edges:
            pos_v = edge._Arista__pair[0].attrib['position']
            pos_u = edge._Arista__pair[1].attrib['position']
            delta_e = pos_v - pos_u
            dist_e = np.linalg.norm(delta_e) #euclidian distance
            f_attr = (dist_e**2) / self.k
            if dist_e <=0:
                dist_e = 0.000000001
            edge._Arista__pair[0].attrib['displacement'] = edge._Arista__pair[0].attrib['displacement'] - ((delta_e/dist_e) * f_attr)
            edge._Arista__pair[1].attrib['displacement'] = edge._Arista__pair[1].attrib['displacement'] + ((delta_e/dist_e) * f_attr)

        #update positions
        disp_delta = np.zeros(2)
        for node in self.graph._Grafo__nodes.values():
            d_desp = np.linalg.norm(node.attrib['displacement'])
            disp_delta = disp_delta + (node.attrib['displacement'] / d_desp)
            node.attrib['position'] = node.attrib['position'] + (node.attrib['displacement']/d_desp) * min(d_desp,self.t)

        self.iterations = self.iterations + 1
        self.cooling()

        _disp_delta = np.linalg.norm(disp_delta)
        displacement = _disp_delta - self.displacement_delta

        if self.displacement_boundary > displacement:
            self.count.append(displacement)
        else:
            self.count = []

        self.displacement_delta = _disp_delta

        # control convergence
        if len(self.count) >= self.num_consecutive_convergences:
            self.has_converged = True
