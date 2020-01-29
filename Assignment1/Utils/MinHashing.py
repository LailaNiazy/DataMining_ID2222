# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 12:30:40 2019

@author: looly
"""

import random
import numpy as np

# function to generate some random numbers
def Rand(start, end, num):
    res = []
    for j in range(num):
        res.append(random.randint(start, end))
    return res
    
    #function to get all existing shingles and put them in one set
def getAllshingles(docsAsShingleSets, version, IDs = 0):
    
    AllShingles = set()
    #different versions for different shinglings function
    for i in range(len(docsAsShingleSets)):
        if version == "1":
            c = IDs[i]
        elif version == "2":
                c = i
        AllShingles.update(list(docsAsShingleSets[c]))

    return AllShingles
            


def calcSigMatrix(docAndShingles,numberOfHashFunctions, version, IDs= 0):
    
    existingshingles = getAllshingles(docAndShingles, version, IDs)
    # 2 num shingels is number of rows for the permuting
    numberShingles = len(existingshingles)
    numberOfDocuments = len(docAndShingles)

    # 3 construct the sigMatrix to start with
    sigMatrix = np.full((numberOfHashFunctions,numberOfDocuments),numberShingles)

    # random number generator for 3 functions
    randomNumbers = Rand(0, numberShingles, 2*numberOfHashFunctions)
    
    #check which version and depending on that different primeNumbers are used
    if version == "1":
        primeNum = 10099
    elif version == "2":
        primeNum = 909526

    # 4 pseudocode alg minHash:
    # for each row r do begin
    for index, shingle in enumerate(existingshingles):
        #for each hash function hi do
        i=0
        permutations = []
        
        while i < (len(randomNumbers)/2):
            #(a * i + b) % c
            half = (int(len(randomNumbers) / 2))
            
            permutations.append((randomNumbers[i] *index  + randomNumbers[i + half]  ) % primeNum)

            i=i+1
        # for each column c
        c=0
        
        while c < numberOfDocuments:
            # if c has 1 in row r --> if shingle is in document c
            if version == "1":
                s = IDs[c]
            elif version == "2":
                s = c
                
            if shingle in docAndShingles[s]:
                #for each hash function hi do
                p=0
                while p < len(permutations):
                    # if hi(r) is smaller than M(i,c) then
                    if permutations[p] < sigMatrix[p][c]:
                        # M(i,c) = h(r)
                        sigMatrix[p][c] = permutations[p]
                    p=p+1
            c=c+1

    return sigMatrix