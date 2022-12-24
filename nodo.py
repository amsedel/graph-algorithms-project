from constants import *
import numpy
import random
import pygame

class Nodo:
  #constructor
  def __init__(self, data, color = BLUE, width = NODE_WIDTH) -> None:
      self.__data = data 
      self.attrib = {
        'displacement' : numpy.array([0, 0]),
        'position': numpy.array([random.randrange(MARGIN, SIZE[0]-MARGIN), random.randrange(MARGIN, SIZE[1]-MARGIN)]),
        'position_with_scale': numpy.array([0, 0]),
        'style': {
          'width': width,
          'color': color
        }
      }

  #Get to node
  @property
  def data(self):
    return self.__data

  #Modify special function __eq__ to compare equality of nodes
  def __eq__(self, __o: object) -> bool:
    return self.data == __o.data
  
  #Return node like string
  def __str__(self) -> str:
    return f"{self.data}" 

  #hash value as integer
  def __hash__(self) -> int:
    return hash(self.data)

  def draw(self, canvas):
    pygame.draw.circle(canvas, self.attrib['style']['color'], self.attrib['position_with_scale'], self.attrib['style']['width'])