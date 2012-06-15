'''
Chung/Janson-Luczal graph generator
'''
import os
import networkx as nx
import utils
import matplotlib.pyplot as plt

n = 200
beta = 1.7
mean_degree = 10

G = nx.empty_graph(n)

degreeArray = utils.degreeDistribution(beta, n, mean_degree)

utils.randPairings(G, degreeArray)

"""
output of the RGG
"""
if not os.path.exists('generated'):
    os.mkdir('generated')

txtName = "generated/adj-%s-%s-%s-.txt" % (str(n), str(beta), str(mean_degree))
nx.write_adjlist(G, txtName)

"""
plotting
"""
utils.drawDegreeHistogram(G)
if n < 1000:
    utils.drawGraph(G)
pngname = "generated/graph-%s-%s-%s-.png" % (str(n), str(beta), str(mean_degree))
plt.savefig(pngname)

if not os.path.exists('feed'):
    os.mkdir('feed')

utils.generateFeed(n)

