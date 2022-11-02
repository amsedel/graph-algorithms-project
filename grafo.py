from cmath import inf
from arista import Arista
from nodo import Nodo

class Grafo:

  #constructor
  def __init__(self, is_weighted=False,is_directed=False,is_auto_loop=False) -> None:
    self.__edges = []
    self.__adjacency_list = {}
    self.__is_auto_loop = is_auto_loop
    self.__is_directed = is_directed
    self.__induced_graph = []
    self.__explored = []
    self.__bfs_layers = []
    self.__is_weighted = is_weighted
    self.__custom_nodes = {}


  #Print the list of edges in the graph
  def __str__(self) -> str:
    return str([str(edge) for edge in self.__edges])

  #Build an adjacency nodes dictionary
  def __get_adjacency(self) -> dict:
    self.__adjacency_list.clear()
    for edge in self.__edges:
      node1 = edge.get_Node1()
      node2 = edge.get_Node2()
      if self.__is_directed:
        self.__add_edge_to_dict(node1,node2)
      else:
        self.__add_edge_to_dict(node1,node2)
        self.__add_edge_to_dict(node2,node1)
    return self.__adjacency_list

  #Create or add a node in the adjacency list
  def __add_edge_to_dict(self, node1, node2):
    if node1 in self.__adjacency_list:
      self.__adjacency_list[node1].append([node2])
    else:
      self.__adjacency_list[node1] = [[node2]]
    if node2 not in self.__adjacency_list:
      self.__adjacency_list[node2] = []

  #Add an edge considering if the graph is directed or not or if the graph has loops or not
  def add_edge(self, edge:Arista):
    edge_inv = Arista(edge.get_Node2(),edge.get_Node1())
    if self.__is_directed == False and self.__is_auto_loop == False:
      if edge not in self.__edges and (edge.get_Node1() != edge.get_Node2()) and edge_inv not in self.__edges:
        self.__edges.append(edge)

    if self.__is_directed == False and self.__is_auto_loop == True:
      if edge not in self.__edges and edge_inv not in self.__edges:
        self.__edges.append(edge)

    if self.__is_directed == True and self.__is_auto_loop == False:
      if edge not in self.__edges and (edge.get_Node1() != edge.get_Node2()):
        self.__edges.append(edge)

    if self.__is_directed == True and self.__is_auto_loop == True:
      if edge not in self.__edges:
        self.__edges.append(edge)

  #Return a list of edges and each edge is a tuple
  def edges_list(self):
    edges_list = []
    for edge in self.__edges:
      #edges_list.append(str(edge))
      edges_list.append(tuple(str(edge)[1:-1].split(',')))
    return edges_list

  #Return a dictionary of adjacency nodes
  def adjacency_dict(self) -> dict:
    self.__get_adjacency()
    dict_adj = {}
    for key, values in self.__adjacency_list.items():
      nodes = []
      for value in values:
        nodes = nodes + [str(value[0])]
      dict_adj[str(key)]=nodes
    return dict_adj

  #Return the node degree
  def node_degree(self, node:Nodo) -> int:
    self.__get_adjacency()
    if node in self.__adjacency_list:
      return len(self.__adjacency_list[node])
    else:
      return 0

  #Allows to print the edges and configure the display of the nodes 
  def __custom_graph(self, edges_tuples):
    content = []
    graph_type = 'graph'
    if self.__is_directed == False and self.__custom_nodes=={}:
      content = [f"{str(t[0])}--{str(t[1])}" for t in edges_tuples]
    if self.__is_directed == True and self.__custom_nodes=={}:
      content = [f"{str(t[0])}->{str(t[1])}" for t in edges_tuples]
      graph_type = 'digraph'
    if self.__is_directed == False and len(self.__custom_nodes)>0:
      content = [f"{str(t[0])}--{str(t[1])}" for t in edges_tuples]
      customNodes = [f"{str(n[0])} {str(n[1])}" for n in list(self.__custom_nodes.items())]
      content = content + customNodes
    if self.__is_directed == True and len(self.__custom_nodes)>0:
      content = [f"{str(t[0])}->{str(t[1])}" for t in edges_tuples]
      customNodes = [f"{str(n[0])} {str(n[1])}" for n in list(self.__custom_nodes.items())]
      content = content + customNodes
      graph_type = 'digraph'
    return content, graph_type

  #Save a graph or digraph in a .gv file
  def save_graph(self, file_name:str ='g', n:int=0, edges_list:list=[]):
    if len(edges_list) > 0:
      edges_tuples = [tuple(str(edge)[1:-1].split(',')) for edge in list(edges_list)]
    else:
      edges_tuples = [tuple(str(edge)[1:-1].split(',')) for edge in list(self.__edges)]

    content, graph_type = self.__custom_graph(edges_tuples)
    self.__custom_nodes = {}

    with open(file_name+'_'+graph_type+'_n_'+str(n)+'.gv', 'w') as f:
      f.write(graph_type + ' ' + file_name +'{\n')
      for d in content:
        f.write(d + '\n')
      f.write('}'+ '\n')
    f.close()

  #Find if a graph it is bipartite through the BFS algorithm
  def is_bipartite(self):
    self.BFS(1)
    for l in self.__bfs_layers:
      if len(l)>1:
        for n in range(1,len(l)):
          if (l[n-1],l[n]) in self.edges_list() or (l[n],l[n-1]) in self.edges_list():
            return False
    return True


  #BFS algorithm
  def BFS(self, s):
    # s: any source node of the graph
    self.__induced_graph, self.__bfs_layers = [], [] #clean variables
    discovered = { str(s) : True}
    i = 0 #layers count
    self.__bfs_layers = [[str(s)]] #initialize layer 0 with s 
    for n_k in self.adjacency_dict().keys():
      if n_k not in discovered:
        discovered[n_k] = False
    while len(self.__bfs_layers[i]) > 0: 
      self.__bfs_layers.append([])
      for u in self.__bfs_layers[i]:
        nodes = self.adjacency_dict()[u]
        for v in nodes:
          if discovered[v] == False:
            discovered[v] = True
            self.__bfs_layers[i+1].append(v)
            self.__induced_graph.append(Arista(Nodo(u),Nodo(v)))
      i = i + 1
    return [str(edge) for edge in self.__induced_graph]


  #DFS recursive algorithm
  def DFS_R(self, u):
    # u: node
    #Clean at start
    if len(self.__explored) == 0:
      self.__induced_graph = []
    induced_graph = self.__induced_graph
    #Recursive Algorithm
    self.__explored.append(str(u))
    for v in self.adjacency_dict()[str(u)]:
      if v not in self.__explored:
        self.__induced_graph.append(Arista(Nodo(u),Nodo(v)))
        self.DFS_R(v)
    #Clean when finished
    if len(self.adjacency_dict().keys()) == len(self.__explored) and self.__explored[0] == str(u):
      #self.__induced_graph = []
      self.__explored = []
    return [str(edge) for edge in induced_graph]
  
  #DFS iterative algorithm
  def DFS_I(self, s):
    # clean variables
    # s: any source node of the graph
    # d: it is a list of discovered nodes
    self.__induced_graph, dfs_i, d  = [], [], [] 
    self.__explored.append(str(s))
    while len(self.__explored) > 0:
      v = self.__explored.pop()
      if v in d:
        continue
      d.append(str(v))
      nodes = self.adjacency_dict()[str(v)]
      for i in reversed(range(len(nodes))):
        u = nodes[i]
        if str(u) not in d:
          self.__explored.append(u)
    for i in range(1,len(d)):
      #clean variables
      #From discovered nodes order get continuos edges
      if (d[i-1], d[i]) in self.edges_list() or (d[i], d[i-1]) in self.edges_list():
        self.__induced_graph.append(Arista(Nodo(d[i-1]),Nodo(d[i])))
      else:
      #From discovered nodes order find the closest node to other node to form an edge
        for j in reversed(range(i)):
          if (d[j], d[i]) in self.edges_list() or (d[i], d[j]) in self.edges_list():
            self.__induced_graph.append(Arista(Nodo(d[j]),Nodo(d[i])))
            break
    dfs_i = self.__induced_graph
    self.__induced_graph = []
    return [str(edge) for edge in dfs_i]

  #gives dictionary format to the edges with weight
  # { "(node1,node2)" : weight}
  def weighted_edges(self) -> dict:
    weighted_edges_dict = {}
    if self.__is_weighted == True:
      for edge in self.edges_list():
        weighted_edges_dict[(str(edge[0]),str(edge[1]))]=float(edge[2])
    return weighted_edges_dict

  #Finds the node with the minimun weight and update the queue (q)
  def __priority_queue(self, weight_list, nodes_list, q):
    if len(q) > 0:
      n,w = map(list,zip(*[v for v in zip(nodes_list,weight_list) if v[0] in q]))
      index = w.index(min(w))
      item = n[index]
      q.remove(item)
      return [item] + q
    else:
      return []

  # Dijkstra algorithm
  def Dijkstra(self, s):
    # s: source node
    # q: priority queue
    # S: coverage
    # d: relation between nodes and weights: {Node1: weight}
    # tree: relation of nodes and edges: {Node2:(Node1,Node2)}
    q, S, self.__induced_graph = [], [], []
    d, tree = {}, {}
    for n in self.adjacency_dict().keys():
      if n != str(s):
        q.append(n)
        d[n] = inf
    q = [str(s)] + q
    d[str(s)] = 0.0
    w_e = self.weighted_edges()
    while len(q) > 0:
      u = q.pop(0)
      S.append(str(u))
      for v in self.adjacency_dict()[str(u)]:
        if self.__is_directed:
          if v not in S and (u,v) in w_e:
            if d[v] > (d[u] + w_e[(u,v)]):
              d[v] = round(float(d[u] + w_e[(u,v)]),2)
              tree[v] = (int(u), int(v))
        else:
          if v not in S:
            l_e = w_e[(u,v)] if (u,v) in w_e else w_e[(v,u)]
            if d[v] > (d[u] + l_e):
              d[v] = round(float(d[u] + l_e),2)
              tree[v] = (int(u), int(v))

      q = self.__priority_queue(list(d.values()),list(d.keys()),q)
    self.__custom_nodes = {key: f'[label="{key}({str(value)})"]' for (key,value) in d.items()}
    self.__induced_graph=[Arista(Nodo(tree[k][0]),Nodo(tree[k][1])) for k in list(tree.keys())]
    return [str(edge) for edge in self.__induced_graph]
