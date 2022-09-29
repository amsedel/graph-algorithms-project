class Nodo:
  #constructor
  def __init__(self, data) -> None:
      self.__data = data 

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