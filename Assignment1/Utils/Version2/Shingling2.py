# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 16:00:59 2019

@author: looly
"""

# A class Shingling that constructs k–shingles of a given length k (e.g., 10) from a given document,
# computes a hash value for each unique shingle,
# and represents the document in the form of an ordered set of its hashed k-shingles.


# 2. shingle
# hash if h = TRUE
def shingle(document, k, h):
    # change this to set if necessary
    shingles = set()
    i = 0
    while i < (len(document) - (k + 1)):
        shingle = document[i:i + k]
        if h:
            shingle = hash(shingle)
            #shingle = hashlib.sha1(shingle.encode()).hexdigest()[:8]
        shingles.add(shingle)
        #print(shingle)
        i=i+1

    return shingles

def getdocAsShingles(filepath,shingleSize):
    docAsShingles = dict()
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
             # 2. shingle each line
             # hash shingles if h=True
            shingles = shingle(line, shingleSize, h=True)
             # save all shingles for the documents
            docAsShingles[cnt]=shingles
    return docAsShingles