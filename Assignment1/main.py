# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:01:49 2019

@author: looly
"""

from Utils.Version1.Shingling1 import shingling, jaccard
from Utils.Version2.Shingling2 import getdocAsShingles
from Utils.Version2.CompareSets import jaccardSimilarity,rSubset
from Utils.MinHashing import calcSigMatrix
import sys
from Utils.CompareSignatures import sigSimilarity
from Utils.LHS import doLSH
import os


def main(version,k, numberOfHashFunctions, threshold):
    

    path = "./DataSet/articles_10.txt"
    #check if file in path exists otherwise terminate the run
    if not os.path.isfile(path):
        print("File path {} does not exist. Exiting...".format(path))
        sys.exit()
          
    if version == "1":
    
        print('\n################ Version 1 Shingling ####################')
        IDs, docsAsShingleSets = shingling(path,k)
        similar_docs = jaccard(IDs,docsAsShingleSets,threshold)
        print('\n################ Version 1 Jaccard Similar items ####################')
        print('According to Shingling similar Documents are')
        print(similar_docs)
        print('\n################ Calculating the signature matrix ####################')
        sigMatrix = calcSigMatrix(docsAsShingleSets,numberOfHashFunctions, version, IDs)
        
        print('Signature Matrix is')
        print(sigMatrix)
        
    elif version == "2":
        print('\n################ Version 2 Shingling ####################')
        docsAsShingleSets = getdocAsShingles(path,k)
        # Get all permutations of length 2
        array = []
        [array.append(i) for i in range(len(docsAsShingleSets))]
        perm = rSubset(array,2)
        print('\n################ Version 2 Jaccard Similar items ####################')
        for i in list(perm):
            #  jaccard sim
            jaccSim = jaccardSimilarity(docsAsShingleSets[i[0]], docsAsShingleSets[i[1]])
        
            if jaccSim >= threshold:
                print('According to Shingling jaccard similarity: %f for documents: %d and %d' % (jaccSim, i[0], i[1] ))
        print('\n################ Calculating the signature matrix ####################')
        sigMatrix = calcSigMatrix(docsAsShingleSets,numberOfHashFunctions, version)
        print('Signature Matrix is')
        print(sigMatrix)
    else:
        print("Version doesn't exist")
        sys.exit()
   
    
    _ ,  similar_docs2 = sigSimilarity(sigMatrix,threshold)
    print('According to Minhash similar Documents are')
    print(similar_docs2)
    print('\n################ LSH ####################')
    lhsList = doLSH(sigMatrix, threshold, version)
    
    print('According to LSH similar Documents are')
    print(lhsList)
    jaccLhsList = []
#
#    # 6. Optional: remove false negatives by coparing the jaccard similarity
    for candidate in lhsList:
        if version == '1':
            c1 = IDs[candidate[0]]
            c2 = IDs[candidate[1]] 
        elif version == '2':
            c1 = candidate[0]
            c2 = candidate[1]            
        jsim = jaccardSimilarity(docsAsShingleSets[c1], docsAsShingleSets[c2])
        if jsim >= threshold:
            jaccLhsList.append((candidate,jsim))

    print('LSH SIMILAR ITEMS AFTER COMPARING THE JACCARD SIMILARITY OF SIMILAR ITEMS TO REMOVE FALSE POSITIVES:')
    print(jaccLhsList)



        
    
if __name__ == "__main__": 
    #input in the console is the number of the task
    version = input("Enter the version to be performed: ")
    
    k = input("Enter the shingle size: ")
    
    if k == '':
       k = 10
    else:
        k = int(k)
        
    numberOfHashFunctions = input("Enter the number of hash functions: ")
    
    if numberOfHashFunctions == '':
       numberOfHashFunctions = 8
    else:
       numberOfHashFunctions = int(numberOfHashFunctions)
         
    threshold = input("Enter a threshold: ")
    
    if threshold == '':
        threshold = 0.6
    else:
        threshold = float(threshold)
        
    main(version, k, numberOfHashFunctions, threshold)
