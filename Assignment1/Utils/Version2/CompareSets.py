# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 16:00:14 2019

@author: looly
"""

# A class CompareSets that computes the Jaccard similarity of two sets of integers –
# two sets of hashed shingles.

# Function which returns subset or r length from n
from itertools import combinations

def rSubset(arr, r):
    # return list of all subsets of length r
    # to deal with duplicate subsets use
    # set(list(combinations(arr, r)))
    return list(combinations(arr, r))
    

# for sets
def jaccardSimilarity(shingle1, shingle2):
    intersec = len(shingle1.intersection(shingle2))
    union = len(shingle1.union(shingle2))
    #print(intersec)
    #print(union)
    #print(intersec/float(union))
    jsimilarity = intersec/float(union)
    return jsimilarity