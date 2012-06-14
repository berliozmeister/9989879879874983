'''
Chung/Janson-Luczal graph generator
'''
import networkx as nx
import utils

n = 10000
beta = 1.7
mean_degree = 100

G = nx.empty_graph(n)

nx.write_adjlist(G, "a.txt")

degreeArray = utils.degreeDistribution(beta, n, mean_degree)

utils.randPairings(G, degreeArray)

txtName = "adj-%s-%s-%s-" % (str(n), str(beta), str(mean_degree))

nx.write_adjlist(G, txtName)

