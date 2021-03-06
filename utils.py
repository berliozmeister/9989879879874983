'''
Created on 24.05.2012

@author: berlioz

some auxilary functions and classes to be defined here
'''
import numpy as np
import os
import random as rnd
import matplotlib.pyplot as plt
import networkx as nx
import markovgen as mg
#from Crypto.Random import random as rnd
#pass



#def is_valid_degree_sequence(sequence):
    



def weightDistribution(beta, n):
    """
    Generates power-law distributed random variable lying in borders [d_min, d_max]
    """
    u = 1.0 - rnd.random() # u \in R[0,1]
    d_min = 1.0 # min degree
    d_max = n*1.0 # max degree
    tmpPower = 1.0 - beta
    intConst = pow(d_max, tmpPower) - pow(d_min, tmpPower)
    return pow(intConst*u + pow(d_min, tmpPower), 1.0/tmpPower)

def degreeDistribution(beta, n, mean_degree):
    """
    Generates a power law degree distribution of size n with power beta, and average degree mean_degree
    """
    powerLawSeq = [0]*n
    for i in xrange(n):
        powerLawSeq[i] = weightDistribution(beta, n)
    powerLawArray = np.array(powerLawSeq)
    expectedSum = mean_degree*1.0*n
    initialSum = np.sum(powerLawArray)
    for i in xrange(n):
        powerLawArray[i] = powerLawArray[i] * expectedSum / initialSum
    degreeArray = np.array(powerLawArray, dtype = np.longlong)
    return degreeArray
    
def randPairings(G, arr):
    """
    Adds edges to graph G according to random pairings algorithm using array of degrees
    """
    someCounter = 0
    sumOfDegrees = arr.sum()
    # generates a delimiter array consisting of partial sums of given array
    delimiterArray = np.cumsum(arr)
    while someCounter < sumOfDegrees/2:
        G.add_edge(np.searchsorted(delimiterArray, rnd.randrange(sumOfDegrees)),
               np.searchsorted(delimiterArray, rnd.randrange(sumOfDegrees)))
        someCounter += 1

def drawDegreeHistogram(G):
    """
    Draws degree histogram of the graph
    """
    degreeSequence = sorted(nx.degree(G).values(), reverse=True)
    plt.clf()
    plt.cla()
    plt.loglog(degreeSequence, 'b-', marker='o')
    plt.title("Degree rank plot")
    plt.ylabel("degree")
    plt.xlabel("rank")
    
def drawGraph(G):
    """
    Draws the graph structure. Not applicable for graphs with n > 1000.
    """
    plt.axes([0.45, 0.45, 0.45, 0.45])
    plt.cla()
    Gcc = nx.connected_component_subgraphs(G)[0]
    pos = nx.spring_layout(Gcc)
    plt.axis('off')
    nx.draw_networkx_nodes(Gcc, pos, node_size=20)
    nx.draw_networkx_edges(Gcc, pos, alpha=0.4)
    
def generateMsg():
    """
    Generates random message consisting of 15 words
    """
    inputText = open('jeeves.txt')
    markov = mg.Markov(inputText)
    text = markov.generate_markov_text(15) + '\n'
    return text

def generateUserFeed(i):
    """
    Generates feed of up to 15 messages for user # i
    """
    filename = "feed/%s_feed.txt" % str(i)
    f = open(filename, 'a')
    numberOfMessages = rnd.randrange(1, 15)
    for j in range(numberOfMessages):
        messageID = str(i) + "." + str(j)
        res = messageID + " " + generateMsg()
        f.write(res)
    #f.close()
    return numberOfMessages
        

def generateFeed(n):
    """
    Generate feed for all n users where n is number of vertices of the graph
    """        
    msgNumArray = np.empty(n, dtype = int) # array where we keep number of messages
    for i in range(n):
        msgNumArray[i] = generateUserFeed(i)
    print msgNumArray
        


