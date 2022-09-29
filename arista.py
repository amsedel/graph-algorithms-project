from nodo import Nodo

class Arista:
  #constructor
  def __init__(self, nodo1:Nodo, nodo2:Nodo) -> None:
      self.__pair = [nodo1, nodo2]
  
  #Get nodes pair
  def get_pair(self) -> list:
    return self.__pair

  #Return string with the nodes that form edge
  def __str__(self) -> str:
    return f"({self.get_Node1()},{self.get_Node2()})"
  
  #By default Arista is undirected
  def directed(self) -> bool:
    return False

  #def weighted(self) -> bool:
  #  return False

  # Get node 1
  def get_Node1(self) -> Nodo:
    return self.get_pair()[0]

  # Get node 2
  def get_Node2(self) -> Nodo:
    return self.get_pair()[1]
  
  #Modify especial funcion __eq__ to correctly compare a pair of nodes
  def __eq__(self, __o: object) -> bool:
      return self.get_pair()[0] == __o.get_pair()[0] and self.get_pair()[1] == __o.get_pair()[1] 
