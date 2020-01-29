# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 12:45:59 2019

@author: looly
"""

import itertools

def sigSimilarity(sigMatrix,threshold=0.6):
    
    #since we use it once with the whole sigMatrix and once to compare only to documents
    #we have implement an if function to check how many documents/signatures we are comparing
    if sigMatrix.shape[0] == 2:
        count = 0
        for k in range(0, sigMatrix.shape[1]):
            #compare each row of two documents
            count = count + (sigMatrix[0,k] == sigMatrix[1,k])
        sigsimilarity = count / sigMatrix.shape[1]
        
        similar_items = 0
    else:  
        r = []
        similar_items = []
        [r.append(i) for i in range(sigMatrix.shape[1])]
        #get all combinations of the documents we can compare
        for subset in itertools.combinations(r,2):
            count = 0
            for k in range(0, len(sigMatrix)):
                #compare two column by iterating and comparing the rows 
                count = count + (sigMatrix[k,subset[0]] == sigMatrix[k,subset[1]])
            sigsimilarity = count / len(sigMatrix)
            if sigsimilarity >= threshold:
                #if two documents are similar and exceed a certian threshold they are put 
                # in the following list
                    similar_items.append((subset, sigsimilarity))
                
    return sigsimilarity, similar_items