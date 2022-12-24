from cmath import inf
from arista import Arista
from nodo import Nodo
from distributions import Spring
from interface import Scale

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
    self.__custom_edges = {}
    self.__visited = []
    self.__nodes = {}


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
    if str(edge.get_Node1()) not in self.__nodes:
      self.__nodes[str(edge.get_Node1())] = edge.get_Node1()
    if str(edge.get_Node2()) not in self.__nodes:
      self.__nodes[str(edge.get_Node2())] = edge.get_Node2()

    edge_inv = Arista(self.__nodes[str(edge.get_Node2())],self.__nodes[str(edge.get_Node1())])
    if self.__is_directed == False and self.__is_auto_loop == False:
      if edge not in self.__edges and (edge.get_Node1() != edge.get_Node2()) and edge_inv not in self.__edges:
        if self.__is_weighted:
          self.__edges.append(Arista(self.__nodes[str(edge.get_Node1())], self.__nodes[str(edge.get_Node2())], edge.get_weight()))
        else:
          self.__edges.append(Arista(self.__nodes[str(edge.get_Node1())], self.__nodes[str(edge.get_Node2())]))

    if self.__is_directed == False and self.__is_auto_loop == True:
      if edge not in self.__edges and edge_inv not in self.__edges:
        if self.__is_weighted:
          self.__edges.append(Arista(self.__nodes[str(edge.get_Node1())], self.__nodes[str(edge.get_Node2())], edge.get_weight()))
        else:
          self.__edges.append(Arista(self.__nodes[str(edge.get_Node1())], self.__nodes[str(edge.get_Node2())]))

    if self.__is_directed == True and self.__is_auto_loop == False:
      if edge not in self.__edges and (edge.get_Node1() != edge.get_Node2()):
        if self.__is_weighted:
          self.__edges.append(Arista(self.__nodes[str(edge.get_Node1())], self.__nodes[str(edge.get_Node2())], edge.get_weight()))
        else:
          self.__edges.append(Arista(self.__nodes[str(edge.get_Node1())], self.__nodes[str(edge.get_Node2())]))

    if self.__is_directed == True and self.__is_auto_loop == True:
      if edge not in self.__edges:
        if self.__is_weighted:
          self.__edges.append(Arista(self.__nodes[str(edge.get_Node1())], self.__nodes[str(edge.get_Node2())], edge.get_weight()))
        else:
          self.__edges.append(Arista(self.__nodes[str(edge.get_Node1())], self.__nodes[str(edge.get_Node2())]))

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
    if self.__is_directed == False and self.__custom_nodes=={} and self.__custom_nodes == {}:
      content = [f"{str(t[0])}--{str(t[1])}" for t in edges_tuples]
    if self.__is_directed == True and self.__custom_nodes=={} and self.__custom_nodes == {}:
      content = [f"{str(t[0])}->{str(t[1])}" for t in edges_tuples]
      graph_type = 'digraph'
    if self.__is_directed == False and len(self.__custom_nodes)>0 and self.__custom_nodes == {}:
      content = [f"{str(t[0])}--{str(t[1])}" for t in edges_tuples]
      customNodes = [f"{str(n[0])} {str(n[1])}" for n in list(self.__custom_nodes.items())]
      content = content + customNodes
    if self.__is_directed == True and len(self.__custom_nodes)>0 and self.__custom_nodes == {}:
      content = [f"{str(t[0])}->{str(t[1])}" for t in edges_tuples]
      customNodes = [f"{str(n[0])} {str(n[1])}" for n in list(self.__custom_nodes.items())]
      content = content + customNodes
      graph_type = 'digraph'
    if self.__is_directed == False and len(self.__custom_edges)>0 and len(self.__custom_nodes)>0:
      for (u,v) in edges_tuples:
        if (u,v) in self.__custom_edges: 
          content.append(f"{str(u)}--{str(v)} [label={self.__custom_edges[(u,v)]}]")
        else:
          content.append(f"{str(v)}--{str(u)} [label={self.__custom_edges[(v,u)]}]")
      customNodes = [f"{str(n[0])} {str(n[1])}" for n in list(self.__custom_nodes.items())]
      content = content + customNodes
    if self.__is_directed == True and len(self.__custom_edges)>0 and len(self.__custom_nodes)>0:
      content = [f"{str(t[0])}->{str(t[1])} [label={self.__custom_edges[t]}]" for t in edges_tuples]
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
    self.__custom_edges = {}

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

  #Return the edges of a graph without the weighted
  def just_edges(self):
    if self.__is_weighted:
      return [(u,v) for (u,v,w) in self.edges_list()]
    else:
      return self.edges_list()

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
      self.__explored = []
    return [str(edge) for edge in induced_graph]
  
  #DFS iterative algorithm
  def DFS_I(self, s):
    # clean variables
    # s: any source node of the graph
    # d: it is a list of discovered nodes
    self.__induced_graph, dfs_i, d, self.__visited  = [], [], [], []
    self.__explored.append(str(s))
    e = self.just_edges()
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
      if (d[i-1], d[i]) in e or (d[i], d[i-1]) in e:
        self.__induced_graph.append(Arista(Nodo(d[i-1]),Nodo(d[i])))
      else:
      #From discovered nodes order find the closest node to other node to form an edge
        for j in reversed(range(i)):
          if (d[j], d[i]) in e or (d[i], d[j]) in e:
            self.__induced_graph.append(Arista(Nodo(d[j]),Nodo(d[i])))
            break
    dfs_i = self.__induced_graph
    self.__visited = d
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

  """
  Sort algorithm "quicksort" to edges with the minimal cost
  order=ascending :param, if the algorithm is sorted ascending
  order=descending :param, if the algorithm is sorted descending
  values=[(node1,node2, weight), ...] :param, list of edges
  """
  def quicksort(self, values, order="ascending"):
    if len(values) < 1: return []
    left, right, pivot = [], [], values[0]
    for i in range(1,len(values)):
      if order == 'ascending':
        if float(values[i][2]) <= float(pivot[2]):
          left.append(values[i])
        else:
          right.append(values[i])
      else:
        if float(values[i][2]) >= float(pivot[2]):
          left.append(values[i])
        else:
          right.append(values[i])
    return [*self.quicksort(left, order), pivot, *self.quicksort(right, order)]

  """
  Find the connected component for KruskalD
  connected_K = {'node1':node, ...} :param, it is a dictionary of nodes
  i = Node :param
  """
  def find_connected_component(self, connected_K, i):
    if connected_K[i] == i: return i
    return self.find_connected_component(connected_K, connected_K[i])

  """
  Join connected components
  connected_K={'node1':node, ...}:param, dictionary with all  connected componentes
  rank={'node1':int, ...} :param, dictionary with the number of connected elements in the connected components
  x=connected component 1:param
  y=connected component 2:param
  """
  def merge_trees(self, connected_K, rank, x, y):
    if rank[x] < rank[y]: connected_K[x] = y
    elif rank[x] > rank[y]: connected_K[y] = x
    else:
      connected_K[y] = x
      rank[x] += 1
  
  """
  Verifies that a tree is still connected through the DFS algorithm
  Comparing the number of nodes of the original graph and those visited by the tree
  originGSize=int(number original graph nodes):param
  """
  def is_connected(self, originGSize):
    n = list(self.adjacency_dict().keys())
    self.DFS_I(n[0])
    if len(self.__visited)==len(originGSize):
      return True
    return False

  """
  Direct Kruskal Algorithm
  """
  def KruskalD(self):
    self.__induced_graph, self.__custom_nodes  = [], {}
    edges_3tuples = [tuple(str(edge)[1:-1].split(',')) for edge in list(self.__edges)]
    sort_edges = self.quicksort(edges_3tuples)
    connected_component = {}
    rank = {}
    total_weight = 0
    for n in self.adjacency_dict().keys():
      connected_component[n] = n
      rank[n] = 0
    s = list(connected_component.keys())[0]
    for (u,v,w) in sort_edges:
      k_u = self.find_connected_component(connected_component,u)
      k_v = self.find_connected_component(connected_component,v)
      if k_u != k_v:
        total_weight += float(w)
        self.__induced_graph.append(Arista(Nodo(u),Nodo(v)))
        self.merge_trees(connected_component,rank, k_u, k_v)
    #print the total weight of the MST on a node
    self.__custom_edges = self.weighted_edges()
    self.__custom_nodes = {str(s): f'[label="{str(s)}, MST = {str(round(total_weight,2))}"]'}
    return [str(edge) for edge in self.__induced_graph]

  """
  Inverse Kruskal Algorithm
  """
  def KruskalI(self):
    self.__custom_nodes = {}
    induced_graph,  total_weight = [], 0
    self.__induced_graph, g_nodes = [], list(self.adjacency_dict().keys())
    edges_4tuples = [tuple(str(e)[1:-1].split(',')) + (self.__edges[i],) for i, e in enumerate(self.__edges)]
    sort_edges = self.quicksort(edges_4tuples, order="descending")

    for (u,v,w,edge) in sort_edges:
      self.__edges.remove(edge)
      if not self.is_connected(g_nodes):
        induced_graph.append(Arista(Nodo(u),Nodo(v)))
        total_weight += float(w)
        self.add_edge(edge)

    self.__edges = [i[3] for i in edges_4tuples]
    self.__custom_edges = self.weighted_edges()
    #print the total weight of the MST on a node
    self.__custom_nodes = {str(g_nodes[0]): f'[label="{str(g_nodes[0])}, MST = {str(round(total_weight,2))}"]'}
    return [str(edge) for edge in induced_graph]

  """
  Prim Algorithm
  """
  def Prim(self):
    q, self.__induced_graph = [], []
    self.__custom_nodes, d, tree, S = {}, {}, {}, {}
    adj = self.adjacency_dict()
    w_e = self.weighted_edges()
    S = {str(n):False for n in adj.keys()}
    d = {str(n):inf for n in adj.keys()}
    q = [str(n) for n in adj.keys()]
    s = q[0]
    d[s] = 0.0
    while len(q) > 0:
      u = q.pop(0)
      S[str(u)] = True
      for v in adj[str(u)]:
        if self.__is_directed:
          if (u,v) in w_e:
            if S[str(v)] == False and l_e < d[str(v)]:
              d[str(v)] = l_e
              tree[v] = (int(u), int(v))
        else:
          l_e = w_e[(u,v)] if (u,v) in w_e else w_e[(v,u)]
          if S[str(v)] == False and l_e < d[str(v)]:
            d[str(v)] = l_e
            tree[v] = (int(u), int(v))
      q = self.__priority_queue(list(d.values()),list(d.keys()),q)
    self.__induced_graph=[Arista(Nodo(tree[k][0]),Nodo(tree[k][1])) for k in list(tree.keys())]
    MST = sum(d.values())
    self.__custom_edges = self.weighted_edges()
    #print the total weight of the MST on a node
    self.__custom_nodes = {str(s): f'[label="{str(s)}, MST = {str(round(MST,2))}"]'}
    return [str(edge) for edge in self.__induced_graph]

  """
  Draw Graphs with pygame and Algorithm "Spring"
  """
  def draw(self, canvas):
    self.__get_adjacency()

    s = Spring(self)
    s.motion()

    scale = Scale(self)
    scale.calculate_scale()

    for node in list(self.__nodes.values()):
      node.attrib['position_with_scale'] = scale.scaling(node.attrib['position'])

    for edge in self.__edges:
      edge.draw(canvas)

    for node in list(self.__nodes.values()):
      node.draw(canvas)
