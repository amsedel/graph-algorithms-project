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
        w = round(random.uniform(0,10),2)
        g.add_edge(Arista(Nodo(i),Nodo(i+1),w)) if ponderado else g.add_edge(Arista(Nodo(i),Nodo(i+1)))
      if i+m<t:
        w = round(random.uniform(0,10),2)
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
      w = round(random.uniform(0,10),2)
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
          w = round(random.uniform(0,10),2)
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
            w = round(random.uniform(0,10),2)
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
          w = round(random.uniform(0,10),2)
          g.add_edge(Arista(Nodo(i),Nodo(j),w)) if ponderado else g.add_edge(Arista(Nodo(i),Nodo(j)))

    while nodes[-1] < n:
      new_node = [len(nodes)+1]
      for i in mutable_nodes:
        p_v = 1-(g.node_degree(Nodo(i))/d)
        if p_v > 0:
          bernoulli = random.random()
          if bernoulli > 0.5:
            w = round(random.uniform(0,10),2)
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
      w1 = round(random.uniform(0,10),2)
      w2 = round(random.uniform(0,10),2)
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
kruskalD_GM_20 = GM_20.KruskalD()
GM_20.save_graph('kruskalD_malla',20, kruskalD_GM_20)
kruskalI_GM_20 = GM_20.KruskalI()
GM_20.save_graph('kruskalI_malla',20, kruskalI_GM_20)
prim_GM_20 = GM_20.Prim()
GM_20.save_graph('prim_malla',20, prim_GM_20)

GM_150 = grafoMalla(15,10,ponderado=True)
kruskalD_GM_150 = GM_150.KruskalD()
GM_150.save_graph('kruskalD_malla',150, kruskalD_GM_150)
kruskalI_GM_150 = GM_150.KruskalI()
GM_150.save_graph('kruskalI_malla',150, kruskalI_GM_150)
prim_GM_150 = GM_150.Prim()
GM_150.save_graph('prim_malla',150, prim_GM_150)
"""

#Grafo Erdos Renyi
"""
GER_20 = grafoErdosRenyi(20,50,ponderado=True)
kruskalD_GER_20 = GER_20.KruskalD()
GER_20.save_graph('kruskalD_Erdos_Renyi',20, kruskalD_GER_20)
kruskalI_GER_20 = GER_20.KruskalI()
GER_20.save_graph('kruskalI_Erdos_Renyi',20, kruskalI_GER_20)
prim_GER_20 = GER_20.Prim()
GER_20.save_graph('prim_Erdos_Renyi',20, prim_GER_20)

GER_150 = grafoErdosRenyi(150,600,ponderado=True)
kruskalD_GER_150 = GER_150.KruskalD()
GER_150.save_graph('kruskalD_Erdos_Renyi',150, kruskalD_GER_150)
kruskalI_GER_150 = GER_150.KruskalI()
GER_150.save_graph('kruskalI_Erdos_Renyi',150, kruskalI_GER_150)
Prim_GER_150 = GER_150.Prim()
GER_150.save_graph('Prim_Erdos_Renyi',150, Prim_GER_150)
"""

#Grafo Gilbert
"""
GG_20 = grafoGilbert(20,0.5,ponderado=True)
KruskalD_GG_20 = GG_20.KruskalD()
GG_20.save_graph('KruskalD_Gilbert',20, KruskalD_GG_20)
KruskalI_GG_20 = GG_20.KruskalI()
GG_20.save_graph('KruskalI_Gilbert',20, KruskalI_GG_20)
Prim_GG_20 = GG_20.Prim()
GG_20.save_graph('Prim_Gilbert',20, Prim_GG_20)

GG_150 = grafoGilbert(150,0.1,ponderado=True)
KruskalD_GG_150 = GG_150.KruskalD()
GG_150.save_graph('KruskalD_Gilbert',150, KruskalD_GG_150)
KruskalI_GG_150 = GG_150.KruskalI()
GG_150.save_graph('KruskalI_Gilbert',150, KruskalI_GG_150)
Prim_GG_150 = GG_150.Prim()
GG_150.save_graph('Prim_Gilbert',150, Prim_GG_150)
"""

#Grafo Geográfico
"""
GGEO_20 = grafoGeografico(20, 0.6, ponderado=True)
KruskalD_GGEO_20 = GGEO_20.KruskalD()
GGEO_20.save_graph('KruskalD_Geografico',20, KruskalD_GGEO_20)
KruskalI_GGEO_20 = GGEO_20.KruskalI()
GGEO_20.save_graph('KruskalI_Geografico',20, KruskalI_GGEO_20)
Prim_GGEO_20 = GGEO_20.Prim()
GGEO_20.save_graph('Prim_Geografico',20, Prim_GGEO_20)

GGEO_150 = grafoGeografico(150, 0.15, ponderado=True)
KruskalD_GGEO_150 = GGEO_150.KruskalD()
GGEO_150.save_graph('KruskalD_Geografico',150, KruskalD_GGEO_150)
KruskalI_GGEO_150 = GGEO_150.KruskalI()
GGEO_150.save_graph('KruskalI_Geografico',150, KruskalI_GGEO_150)
Prim_GGEO_150 = GGEO_150.Prim()
GGEO_150.save_graph('Prim_Geografico',150, Prim_GGEO_150)
"""

#Grafo Barabasi Albert
"""
GBA_20 = grafoBarabasiAlbert(20,5,ponderado=True)
KruskalD_GBA_20 = GBA_20.KruskalD()
GBA_20.save_graph('KruskalD_BarabasiAlbert',20, KruskalD_GBA_20)
KruskalI_GBA_20 = GBA_20.KruskalI()
GBA_20.save_graph('KruskalI_BarabasiAlbert',20, KruskalI_GBA_20)
Prim_GBA_20 = GBA_20.Prim()
GBA_20.save_graph('Prim_BarabasiAlbert',20, Prim_GBA_20)

GBA_150 = grafoBarabasiAlbert(150,6,ponderado=True)
KruskalD_GBA_150 = GBA_150.KruskalD()
GBA_150.save_graph('KruskalD_BarabasiAlbert',150, KruskalD_GBA_150)
KruskalI_GBA_150 = GBA_150.KruskalI()
GBA_150.save_graph('KruskalI_BarabasiAlbert',150, KruskalI_GBA_150)
Prim_GBA_150 = GBA_150.Prim()
GBA_150.save_graph('Prim_BarabasiAlbert',150, Prim_GBA_150)
"""

#Grafo Dorogovtsev Mendes
"""
GDM_20 = grafoDorogovtsevMendes(20, ponderado=True)
KruskalD_GDM_20 = GDM_20.KruskalD()
GDM_20.save_graph('KruskalD_DorogovtsevMendes',20, KruskalD_GDM_20)
KruskalI_GDM_20 = GDM_20.KruskalI()
GDM_20.save_graph('KruskalI_DorogovtsevMendes',20, KruskalI_GDM_20)
Prim_GDM_20 = GDM_20.Prim()
GDM_20.save_graph('Prim_DorogovtsevMendes',20, Prim_GDM_20)

GDM_150 = grafoDorogovtsevMendes(150, ponderado=True)
KruskalD_GDM_150 = GDM_150.KruskalD()
GDM_150.save_graph('KruskalD_DorogovtsevMendes',150, KruskalD_GDM_150)
KruskalI_GDM_150 = GDM_150.KruskalI()
GDM_150.save_graph('KruskalI_DorogovtsevMendes',150, KruskalI_GDM_150)
Prim_GDM_150 = GDM_150.Prim()
GDM_150.save_graph('Prim_DorogovtsevMendes',150, Prim_GDM_150)
"""