'''
Created on 24.05.2012

@author: berlioz

some auxilary functions and classes to be defined here
'''
import numpy as np
import os
import random as rnd
if os.name == 'nt':
    import random as rnd
else:
    from Crypto.Random import random as rnd
pass



def weightDistribution(beta, n):
    """
    Generates power-law distributed random number lying in borders [d_min, d_max]
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
    delimiterArray = np.cumsum(arr) # generates a delimiter array consisting of partial sums of given array
    while someCounter < sumOfDegrees/2:
        G.add_edge(np.searchsorted(delimiterArray, rnd.randrange(sumOfDegrees)),
               np.searchsorted(delimiterArray, rnd.randrange(sumOfDegrees)))
        someCounter += 1
        


