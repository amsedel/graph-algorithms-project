from nodo import Nodo
from constants import *
import pygame

class Arista:
  #constructor overload
  """
  With *args allow to have a single edge (Node1,Node2)
  and allow to have an edge with 3 parameters (Node1, Node2, Weight)
  """
  def __init__(self, *args) -> None:
    self.__has_weight = False
    self.__weight = 0
    if len(args) == 2 and isinstance(args[0],Nodo) and isinstance(args[1],Nodo):
      self.__pair = [args[0], args[1]]
    if len(args) == 3 and isinstance(args[0],Nodo) and isinstance(args[1],Nodo):
      self.__pair = [args[0], args[1]]
      if isinstance(args[2], float) or isinstance(args[2], int):
        self.__has_weight = True
        self.__weight = args[2]
    self.attrib = {
        'style': {
          'width': 1,
          'color': GREEN
        }
      }
  
  #Get nodes pair
  def get_pair(self) -> list:
    return self.__pair
  # Get the weight of the edge
  def get_weight(self) -> float:
    return float(self.__weight)

  #Return string with the nodes that form edge
  def __str__(self) -> str:
    if self.__has_weight:
      return f"({self.get_Node1()},{self.get_Node2()},{self.get_weight()})"
    else:
      return f"({self.get_Node1()},{self.get_Node2()})"
  
  #By default Arista is undirected
  def directed(self) -> bool:
    return False

  # Allow to know if edge has weight
  def has_weight(self) -> bool:
    return self.__has_weight

  # Get node 1
  def get_Node1(self) -> Nodo:
    return self.get_pair()[0]

  # Get node 2
  def get_Node2(self) -> Nodo:
    return self.get_pair()[1]
  
  #Modify especial funcion __eq__ to correctly compare a pair of nodes
  def __eq__(self, __o: object) -> bool:
      return self.get_pair()[0] == __o.get_pair()[0] and self.get_pair()[1] == __o.get_pair()[1] 

  def draw(self, canvas):
    pygame.draw.line(canvas,
                     self.attrib['style']['color'], 
                     self.get_Node1().attrib['position_with_scale'], 
                     self.get_Node2().attrib['position_with_scale'],
                      1)