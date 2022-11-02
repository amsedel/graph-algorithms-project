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
def grafoMalla(m, n, dirigido=False, auto=False, ponderado=False):
  g = Grafo(ponderado, dirigido, auto)
  if m >1 and n>1:
    t = (m*n)+1
    for i in range(1,t):
      if i+1<t and i%m != 0:
        w = round(random.uniform(0,100),2)
        g.add_edge(Arista(Nodo(i),Nodo(i+1),w)) if ponderado else g.add_edge(Arista(Nodo(i),Nodo(i+1)))
      if i+m<t:
        w = round(random.uniform(0,100),2)
        g.add_edge(Arista(Nodo(i),Nodo(i+m),w)) if ponderado else g.add_edge(Arista(Nodo(i),Nodo(i+m)))
    g.save_graph('grafoMalla', m*n)
    return g
  else:
    print("Por favor introduce un valor m>1 y un n>1")



# Modelo Gn,m de Erdös y Rényi. Crear n nodos y elegir uniformemente al azar 
# m distintos pares de distintos vértices.
# :param n: número de nodos (> 0)
# :param m: número de aristas (>= n-1)
# :param dirigido: ¿el grafo es dirigido?
# :param auto: ¿permitir auto-ciclos?
# :return: grafo generado
def grafoErdosRenyi(n, m, dirigido=False, auto=False, ponderado=False):
  g = Grafo(ponderado, dirigido, auto)
  nodes = list(range(1,n+1))

  if m >= (n-1) and n>0:
    while len(g.edges_list()) < m:
      n1 = random.choice(nodes)
      n2 = random.choice(nodes)
      w = round(random.uniform(0,100),2)
      g.add_edge(Arista(Nodo(n1),Nodo(n2),w)) if ponderado else g.add_edge(Arista(Nodo(n1),Nodo(n2)))
    g.save_graph('grafoErdosRenyi', n)
    return g
  else:
    print("Por favor introduce un valor de arista m >= n-1 y un n>0")



# Modelo Gn,p de Gilbert. Crear n nodos y poner una arista entre cada 
# par independiente y uniformemente con probabilidad p.
# :param n: número de nodos (> 0)
# :param p: probabilidad de crear una arista (0, 1)
# :param dirigido: ¿el grafo es dirigido?
# :param auto: ¿permitir auto-ciclos?
# :return: grafo generado
def grafoGilbert(n, p, dirigido=False, auto=False, ponderado=False):
  g = Grafo(ponderado, dirigido, auto)
  nodes = list(range(1,n+1))
  if n>0 and 1>=p>0:
    for i in nodes:
      for j in range(i+1,len(nodes)+1):
        R = random.random() 
        if (R < p):
          w = round(random.uniform(0,100),2)
          g.add_edge(Arista(Nodo(i),Nodo(j),w)) if ponderado else g.add_edge(Arista(Nodo(i),Nodo(j)))
    g.save_graph('grafoGilbert', n)
    return g
  else:
    print("Por favor introduce un valor n>0 y un valor p entre 0 y 1")



#Modelo Gn,r geográfico simple. Colocar n nodos en un rectángulo 
# unitario con coordenadas uniformes (o normales) y colocar una 
# arista entre cada par que queda en distancia r o menor.
# :param n: número de nodos (> 0)
# :param r: distancia máxima para crear un nodo (0, 1)
# :param dirigido: ¿el grafo es dirigido?
# :param auto: ¿permitir auto-ciclos?
# :return: grafo generado
def grafoGeografico(n, r, dirigido=False, auto=False, ponderado=False):
  g = Grafo(ponderado, dirigido, auto)
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
            w = round(random.uniform(0,100),2)
            g.add_edge(Arista(Nodo(node1),Nodo(node2),w)) if ponderado else g.add_edge(Arista(Nodo(node1),Nodo(node2)))
    g.save_graph('grafoGeografico', n)
    return g
  else:
    print("Por favor introduce un valor n>0 y un valor r entre 0 y 1")



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
def grafoBarabasiAlbert(n, d, dirigido=False, auto=False, ponderado=False):
  g = Grafo(ponderado, dirigido, auto)
  initial_nodes = list(range(1,d+1))
  nodes = initial_nodes
  nodes_complete = []
  mutable_nodes = nodes
  if n>0 and d>1:
    for i in initial_nodes:
      for j in initial_nodes:
        if (i < j):
          w = round(random.uniform(0,100),2)
          g.add_edge(Arista(Nodo(i),Nodo(j),w)) if ponderado else g.add_edge(Arista(Nodo(i),Nodo(j)))

    while nodes[-1] < n:
      new_node = [len(nodes)+1]
      for i in mutable_nodes:
        p_v = 1-(g.node_degree(Nodo(i))/d)
        if p_v > 0:
          bernoulli = random.random()
          if bernoulli > 0.5:
            w = round(random.uniform(0,100),2)
            g.add_edge(Arista(Nodo(i),Nodo(new_node[0]),w)) if ponderado else g.add_edge(Arista(Nodo(i),Nodo(new_node[0])))
        else:
          nodes_complete.append(i)
        mutable_nodes = [node for node in mutable_nodes if node not in nodes_complete]    
      nodes = nodes + new_node
      mutable_nodes = mutable_nodes + new_node
    g.save_graph('grafoBarabasiAlbert', n)
    return g
  else:
    print("Por favor introduce un valor n>0 y un valor d>1")



# Modelo Gn Dorogovtsev-Mendes. Crear 3 nodos y 3 aristas formando un triángulo.
# Después, para cada nodo adicional, se selecciona una arista al azar y se crean 
# aristas entre el nodo nuevo y los extremos de la arista seleccionada.
# Genera grafo aleatorio con el modelo Barabasi-Albert
# :param n: número de nodos (≥ 3)
# :param dirigido: ¿el grafo es dirigido?
# :return: grafo generado
def grafoDorogovtsevMendes(n, dirigido=False, auto=False, ponderado=False):
  g = Grafo(ponderado, dirigido, auto)
  if n>=3:
    nodes = list(range(1,4)) #triangle
    g = grafoBarabasiAlbert(3, 3, dirigido, auto, ponderado)
    aux_edges_list = g.edges_list()
    while len(nodes)<n:
      new_node = [len(nodes)+1]
      choice_edge = random.choice(aux_edges_list)
      w1 = round(random.uniform(0,100),2)
      w2 = round(random.uniform(0,100),2)
      g.add_edge(Arista(Nodo(choice_edge[0]),Nodo(new_node[0]),w1)) if ponderado else g.add_edge(Arista(Nodo(choice_edge[0]),Nodo(new_node[0])))
      g.add_edge(Arista(Nodo(choice_edge[1]),Nodo(new_node[0]),w2)) if ponderado else g.add_edge(Arista(Nodo(choice_edge[1]),Nodo(new_node[0])))
      nodes = nodes + new_node
      aux_edges_list.remove(choice_edge)
      aux_edges_list = aux_edges_list + [(choice_edge[0],new_node[0]),(choice_edge[1],new_node[0])]
    g.save_graph('grafoDorogovtsevMendes', n)
    return g
  else:
    print("Por favor introduce un valor n>=3")



#Grafo Malla
"""
GM_20 = grafoMalla(5,4,ponderado=True)
dijkstra_GM_20 = GM_20.Dijkstra(1)
GM_20.save_graph('dijkstra_malla',20, dijkstra_GM_20)

GM_200 = grafoMalla(20,10,ponderado=True)
dijkstra_GM_200 = GM_200.Dijkstra(1)
GM_200.save_graph('dijkstra_malla',200, dijkstra_GM_200)
"""

#Grafo Erdos Renyi
"""
GER_20 = grafoErdosRenyi(20,50,ponderado=True)
dijkstra_GER_20 = GER_20.Dijkstra(1)
GER_20.save_graph('dijkstra_Erdos_Renyi',20, dijkstra_GER_20)

GER_200 = grafoErdosRenyi(200,700,ponderado=True)
dijkstra_GER_200 = GER_200.Dijkstra(1)
GER_200.save_graph('dijkstra_Erdos_Renyi',200, dijkstra_GER_200)
"""

#Grafo Gilbert
"""
GG_20 = grafoGilbert(20,0.5,ponderado=True)
dijkstra_GG_20 = GG_20.Dijkstra(1)
GG_20.save_graph('dijkstra_Gilbert',20, dijkstra_GG_20)

GG_200 = grafoGilbert(200,0.1,ponderado=True)
dijkstra_GG_200 = GG_200.Dijkstra(1)
GG_200.save_graph('dijkstra_Gilbert',200, dijkstra_GG_200)
"""

#Grafo Geográfico
"""
GGEO_20 = grafoGeografico(20, 0.8, ponderado=True)
dijkstra_GGEO_20 = GGEO_20.Dijkstra(1)
GGEO_20.save_graph('dijkstra_Geografico',20, dijkstra_GGEO_20)

GGEO_200 = grafoGeografico(200, 0.15, ponderado=True)
dijkstra_GGEO_200 = GGEO_200.Dijkstra(1)
GGEO_200.save_graph('dijkstra_Geografico',200, dijkstra_GGEO_200)
"""

#Grafo Barabasi Albert
"""
GBA_20 = grafoBarabasiAlbert(20,4,ponderado=True)
dijkstra_GBA_20 = GBA_20.Dijkstra(1)
GBA_20.save_graph('dijkstra_BarabasiAlbert',20, dijkstra_GBA_20)

GBA_200 = grafoBarabasiAlbert(200,6,ponderado=True)
dijkstra_GBA_200 = GBA_200.Dijkstra(1)
GBA_200.save_graph('dijkstra_BarabasiAlbert',200, dijkstra_GBA_200)
"""

#Grafo Dorogovtsev Mendes
"""
GDM_20 = grafoDorogovtsevMendes(20, ponderado=True)
dijkstra_GDM_20 = GDM_20.Dijkstra(1)
GDM_20.save_graph('dijkstra_DorogovtsevMendes',20, dijkstra_GDM_20)

GDM_200 = grafoDorogovtsevMendes(200, ponderado=True)
dijkstra_GDM_200 = GDM_200.Dijkstra(1)
GDM_200.save_graph('dijkstra_DorogovtsevMendes',200, dijkstra_GDM_200)
"""