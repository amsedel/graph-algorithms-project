import random
from nodo import Nodo
from arista import Arista
from grafo import Grafo


#Modelo G(m,n) de malla. Crear m*n nodos. 
# Para el nodo ni,j crear una arista con el nodo ni+1,j y otra 
# con el nodo ni,j+1, para i<m y j<n
#:param m: número de columnas (> 1)
#:param n: número de filas (> 1)
#:param dirigido: ¿el grafo es dirigido?
#:return: grafo generado
def grafoMalla(m, n, dirigido=False, auto=False):
  g = Grafo()
  g.set_is_directed(dirigido)
  g.set_auto_loop(auto)
  if m >1 and n>1:
    t = (m*n)+1
    for i in range(1,t):
      if i+1<t and i%m != 0:
        g.add_edge(Arista(Nodo(i),Nodo(i+1)))
      if i+m<t:
        g.add_edge(Arista(Nodo(i),Nodo(i+m)))
    g.save_graph('grafoMalla', m*n)
    return g
  else:
    print("Por favor introduce un valor m>1 y un n>1")


grafoMalla(6, 5)
grafoMalla(30, 10)
grafoMalla(50, 10)


# Modelo Gn,m de Erdös y Rényi. Crear n nodos y elegir uniformemente al azar 
# m distintos pares de distintos vértices.
# :param n: número de nodos (> 0)
# :param m: número de aristas (>= n-1)
# :param dirigido: ¿el grafo es dirigido?
# :param auto: ¿permitir auto-ciclos?
# :return: grafo generado
def grafoErdosRenyi(n, m, dirigido=False, auto=False):
  g = Grafo()
  g.set_is_directed(dirigido)
  g.set_auto_loop(auto)

  nodes = list(range(1,n+1))

  if m >= (n-1) and n>0:
    while len(g.edges_list()) < m:
      n1 = random.choice(nodes)
      n2 = random.choice(nodes)
      g.add_edge(Arista(Nodo(n1),Nodo(n2)))
    g.save_graph('grafoErdosRenyi', n)
    return g
  else:
    print("Por favor introduce un valor de arista m >= n-1 y un n>0")


grafoErdosRenyi(30,80)
grafoErdosRenyi(300,1000)
grafoErdosRenyi(500,2100)


# Modelo Gn,p de Gilbert. Crear n nodos y poner una arista entre cada 
# par independiente y uniformemente con probabilidad p.
# :param n: número de nodos (> 0)
# :param p: probabilidad de crear una arista (0, 1)
# :param dirigido: ¿el grafo es dirigido?
# :param auto: ¿permitir auto-ciclos?
# :return: grafo generado
def grafoGilbert(n, p, dirigido=False, auto=False):
  g = Grafo()
  g.set_is_directed(dirigido)
  g.set_auto_loop(auto)
  nodes = list(range(1,n+1))
  if n>0 and 1>=p>0:
    for i in nodes:
      for j in range(i+1,len(nodes)+1):
        R = random.random() 
        if (R < p):
          g.add_edge(Arista(Nodo(i),Nodo(j)))
    g.save_graph('grafoGilbert', n)
    return g
  else:
    print("Por favor introduce un valor n>0 y un valor p entre 0 y 1")

grafoGilbert(30,0.5)
grafoGilbert(300,0.1)
grafoGilbert(500,0.04)


#Modelo Gn,r geográfico simple. Colocar n nodos en un rectángulo 
# unitario con coordenadas uniformes (o normales) y colocar una 
# arista entre cada par que queda en distancia r o menor.
# :param n: número de nodos (> 0)
# :param r: distancia máxima para crear un nodo (0, 1)
# :param dirigido: ¿el grafo es dirigido?
# :param auto: ¿permitir auto-ciclos?
# :return: grafo generado
def grafoGeografico(n, r, dirigido=False, auto=False):
  g = Grafo()
  g.set_is_directed(dirigido)
  g.set_auto_loop(auto)
  nodes_positions = []
  nodes = list(range(1,n+1))
  if n>0 and 1>=r>0:
    for i in nodes:
      virtual_position_nx = random.random()
      virtual_position_ny = random.random()
      nodes_positions.append((i,(virtual_position_nx,virtual_position_ny)))

    for (node1,(x1,y1)) in nodes_positions:
      for (node2,(x2,y2)) in nodes_positions:
        if (node1 < node2):
          dist2points = ((x2-x1)**2 + (y2-y1)**2)**0.5
          if(dist2points<=r):
            g.add_edge(Arista(Nodo(node1),Nodo(node2)))
    g.save_graph('grafoGeografico', n)
    return g
  else:
    print("Por favor introduce un valor n>0 y un valor r entre 0 y 1")

grafoGeografico(30, 0.8)
grafoGeografico(300, 0.15)
grafoGeografico(500, 0.1)



# Variante del modelo Gn,d Barabási-Albert. Colocar n nodos uno por uno, 
# asignando a cada uno d aristas a vértices distintos de tal manera que 
# la probabilidad de que el vértice nuevo se conecte a un vértice existente 
# v es proporcional a la cantidad de aristas que v tiene actualmente.
# Los primeros d vértices se conecta todos a todos.
# :param n: número de nodos (> 0)
# :param d: grado máximo esperado por cada nodo (> 1)
# :param dirigido: ¿el grafo es dirigido?
# :param auto: ¿permitir auto-ciclos?
# :return: grafo generado
def grafoBarabasiAlbert(n, d, dirigido=False, auto=False):
  g = Grafo()
  g.set_is_directed(dirigido)
  g.set_auto_loop(auto)
  initial_nodes = list(range(1,d+1))
  nodes = initial_nodes
  nodes_complete = []
  mutable_nodes = nodes
  if n>0 and d>1:
    for i in initial_nodes:
      for j in initial_nodes:
        if (i < j):
          g.add_edge(Arista(Nodo(i),Nodo(j)))

    while nodes[-1] < n:
      new_node = [len(nodes)+1]
      for i in mutable_nodes:
        p_v = 1-(g.node_degree(Nodo(i))/d)
        if p_v > 0:
          bernoulli = random.random()
          if bernoulli > 0.5:
            g.add_edge(Arista(Nodo(i),Nodo(new_node[0])))
        else:
          nodes_complete.append(i)
        mutable_nodes = [node for node in mutable_nodes if node not in nodes_complete]    
      nodes = nodes + new_node
      mutable_nodes = mutable_nodes + new_node
    g.save_graph('grafoBarabasiAlbert', n)
    return g
  else:
    print("Por favor introduce un valor n>0 y un valor d>1")

grafoBarabasiAlbert(30,6)
grafoBarabasiAlbert(300,6)
grafoBarabasiAlbert(500,6)


# Modelo Gn Dorogovtsev-Mendes. Crear 3 nodos y 3 aristas formando un triángulo.
# Después, para cada nodo adicional, se selecciona una arista al azar y se crean 
# aristas entre el nodo nuevo y los extremos de la arista seleccionada.
# Genera grafo aleatorio con el modelo Barabasi-Albert
# :param n: número de nodos (≥ 3)
# :param dirigido: ¿el grafo es dirigido?
# :return: grafo generado
def grafoDorogovtsevMendes(n, dirigido=False):
  g = Grafo()
  g.set_is_directed(dirigido)
  if n>=3:
    nodes = list(range(1,4)) #triangle
    g = grafoBarabasiAlbert(3, 3)
    aux_edges_list = g.edges_list()
    while len(nodes)<n:
      new_node = [len(nodes)+1]
      choice_edge = random.choice(aux_edges_list)
      g.add_edge(Arista(Nodo(choice_edge[0]),Nodo(new_node[0])))
      g.add_edge(Arista(Nodo(choice_edge[1]),Nodo(new_node[0])))
      nodes = nodes + new_node
      aux_edges_list.remove(choice_edge)
      aux_edges_list = aux_edges_list + [(choice_edge[0],new_node[0]),(choice_edge[1],new_node[0])]
    g.save_graph('grafoDorogovtsevMendes', n)
    return g
  else:
    print("Por favor introduce un valor n>=3")

grafoDorogovtsevMendes(30)
grafoDorogovtsevMendes(300)
grafoDorogovtsevMendes(500)
