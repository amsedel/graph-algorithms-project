from generator_algorithms import Graph_Generator
from interface import *
from drawing_algorithms import *


"""
# Clase Spring

# Malla
#gm100_s = Graph_Generator().grafoMalla(10, 10)
#Canvas(gm100_s, Spring(gm100_s)).show()
#gm500_s = Graph_Generator().grafoMalla(25,20)
#Canvas(gm500_s, Spring(gm500_s, c=3)).show()

#Erdos Renyi
#ger100_s = Graph_Generator().grafoErdosRenyi(100, 500)
#Canvas(ger100_s, Spring(ger100_s)).show()
#ger500_s = Graph_Generator().grafoErdosRenyi(500, 2100)
#Canvas(ger500_s, Spring(ger500_s)).show()

#Gilbert
#gg100_s = Graph_Generator().grafoGilbert(100,0.15)
#Canvas(gg100_s, Spring(gg100_s)).show()
#gg500_s = Graph_Generator().grafoGilbert(500,0.02)
#Canvas(gg500_s, Spring(gg500_s)).show()

#Geográfico
#gge100_s = Graph_Generator().grafoGeografico(100, 0.3)
#Canvas(gge100_s, Spring(gge100_s)).show()
#gge500_s = Graph_Generator().grafoGeografico(500, 0.1)
#Canvas(gge500_s, Spring(gge500_s)).show()

#Barabasi Albert
#gba100_s = Graph_Generator().grafoBarabasiAlbert(100,8)
#Canvas(gba100_s, Spring(gba100_s)).show()
#gba500_s = Graph_Generator().grafoBarabasiAlbert(500,5)
#Canvas(gba500_s, Spring(gba500_s)).show()

#Dorogovtsev Mendes
#gdm100_s = Graph_Generator().grafoDorogovtsevMendes(100)
#Canvas(gdm100_s, Spring(gdm100_s)).show()
#gdm500_s = Graph_Generator().grafoDorogovtsevMendes(500)
#Canvas(gdm500_s, Spring(gdm500_s)).show()
"""

 
"""
# Clase Fruchterman Reigold

# Malla
gm100_fr = Graph_Generator().grafoMalla(10, 10)
Canvas(gm100_fr, Fruchterman_Reigold(gm100_fr)).show()
gm500_fr = Graph_Generator().grafoMalla(25, 20)
Canvas(gm500_fr, Fruchterman_Reigold(gm500_fr)).show()

#Erdos Renyi
#ger100_fr = Graph_Generator().grafoErdosRenyi(100, 500)
#Canvas(ger100_fr, Fruchterman_Reigold(ger100_fr)).show()
#ger500_fr = Graph_Generator().grafoErdosRenyi(500, 2100)
#Canvas(ger500_fr, Fruchterman_Reigold(ger500_fr)).show()

#Gilbert
#gg100_fr = Graph_Generator().grafoGilbert(100,0.15)
#Canvas(gg100_fr, Fruchterman_Reigold(gg100_fr)).show()
gg500_fr = Graph_Generator().grafoGilbert(500,0.03)
Canvas(gg500_fr, Fruchterman_Reigold(gg500_fr)).show()

#Geográfico
gge100_fr = Graph_Generator().grafoGeografico(100, 0.2)
Canvas(gge100_fr, Fruchterman_Reigold(gge100_fr)).show()
gge500_fr = Graph_Generator().grafoGeografico(500, 0.1)
Canvas(gge500_fr, Fruchterman_Reigold(gge500_fr)).show()

#Barabasi Albert
#gba100_fr = Graph_Generator().grafoBarabasiAlbert(100,8)
#Canvas(gba100_fr, Fruchterman_Reigold(gba100_fr)).show()
gba500_fr = Graph_Generator().grafoBarabasiAlbert(500,6)
Canvas(gba500_fr, Fruchterman_Reigold(gba500_fr)).show()

#Dorogovtsev Mendes
gdm100_fr = Graph_Generator().grafoDorogovtsevMendes(100)
Canvas(gdm100_fr, Fruchterman_Reigold(gdm100_fr)).show()
gdm500_fr = Graph_Generator().grafoDorogovtsevMendes(500)
Canvas(gdm500_fr, Fruchterman_Reigold(gdm500_fr)).show()

"""

"""
# Clase Barnes Hut

# Malla
gm100_bh = Graph_Generator().grafoMalla(10, 10)
Canvas(gm100_bh, Barnes_Hut(gm100_bh, capacity=5)).show()
gm500_bh = Graph_Generator().grafoMalla(25, 20)
Canvas(gm500_bh, Barnes_Hut(gm500_bh)).show()

#Erdos Renyi
#ger100_bh = Graph_Generator().grafoErdosRenyi(100,500)
#Canvas(ger100_bh, Barnes_Hut(ger100_bh, capacity=16, alpha=4)).show()
#ger500_bh = Graph_Generator().grafoErdosRenyi(500,2100)
#Canvas(ger500_bh, Barnes_Hut(ger500_bh, capacity=18, alpha=1)).show()

#Gilbert
gg100_bh = Graph_Generator().grafoGilbert(100, 0.15)
Canvas(gg100_bh, Barnes_Hut(gg100_bh, capacity=16, alpha=3)).show()
gg500_bh = Graph_Generator().grafoGilbert(500, 0.03)
Canvas(gg500_bh, Barnes_Hut(gg500_bh,capacity=12, alpha=1, boundary = 0.05, num_convergences=30)).show()

#Geográfico
gge100_bh = Graph_Generator().grafoGeografico(100, 0.3)
Canvas(gge100_bh, Barnes_Hut(gge100_bh, capacity=6, alpha=2.2, boundary = 0.00001, num_convergences=100)).show()
gge500_bh = Graph_Generator().grafoGeografico(500, 0.11)
Canvas(gge500_bh, Barnes_Hut(gge500_bh,capacity=16,alpha=1.5, boundary = 0.00001, num_convergences=100)).show()

#Barabasi Albert
gba100_bh = Graph_Generator().grafoBarabasiAlbert(100,10)
Canvas(gba100_bh, Barnes_Hut(gba100_bh, capacity=5, alpha=1.9, boundary = 0.002, num_convergences=25)).show()
gba500_bh = Graph_Generator().grafoBarabasiAlbert(500,8)
Canvas(gba500_bh, Barnes_Hut(gba500_bh, capacity=16, alpha=1.8, boundary = 0.002, num_convergences=25)).show()

#Dorogovtsev Mendes
gdm100_bh = Graph_Generator().grafoDorogovtsevMendes(100)
Canvas(gdm100_bh, Barnes_Hut(gdm100_bh, capacity=10, alpha=8)).show()
gdm500_bh = Graph_Generator().grafoDorogovtsevMendes(500)
Canvas(gdm500_bh, Barnes_Hut(gdm500_bh, capacity=16, alpha=1.2, boundary = 0.003)).show()

"""