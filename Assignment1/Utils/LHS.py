# Optional task for extra 2 bonus) A class LSH that implements the LSH technique:
# given a collection of minhash signatures (integer vectors) and a similarity threshold t,
# the LSH class (using banding and hashing) finds all candidate pairs of signatures
# that agree on at least fraction t of their components.

import numpy as np
import math
from Utils.Version2.CompareSets import rSubset
from Utils.CompareSignatures import sigSimilarity

# General idea: generate from collection of all elements a asmall list of candidate pairs and evaluate the sim of those
# hash columns of sim matrix to man buckets and make elements of the same buckets candidate pairs
# columns are candidate pairs if their signatures agree in a fraction t of the rows

weight = 0.2

def calcLSHList(candidates, sigMatrix, t):
    lshList = []
    for candidate in candidates:
        if len(candidate) > 2:
            candidateSubList = rSubset(candidate,2)
            subcandidate= calcLSHList(candidateSubList, sigMatrix, t)
            for sub in subcandidate:
                lshList.append(sub)
        else:
            matrix= np.array([sigMatrix[:, candidate[0]], sigMatrix[:,candidate[1]]])
            sigsim, _ = sigSimilarity(matrix)
            print(sigsim)
            #print(sigsim)
            if sigsim >= t:
                lshList.append(candidate)
    return lshList


# inRange looks for the value to be close to the t that we want as a threshold
# therefore we define a global weight that we can adjust if needed
def inRange(v,s):
    global weight
    lowLimit=s-weight
    upLimit=s+weight
    if v>lowLimit and v<upLimit:
        return True
    return False


# function to remove possible smaller duplicates from the candidate list
def eachMasterList(allLists):
  allSets = [ set(lst) for lst in allLists ]
  for lst, s in zip(allLists, allSets):
    if not any(s is not otherSet and s < otherSet for otherSet in allSets):
      yield lst

# Function to run the LSH technique
def doLSH(sigMatrix, t, version):
    #number of bands: b
    # number of rows in a band: r
    # number of buckets in a hashtabe: k
    #check which version and depending on that different primeNumbers are used
    if version == "1":
        k = 10099
    elif version == "2":
        k = 909526

    # number of Minhash functions = Length of a signature in the sigMatrix: n
    n = np.size(sigMatrix,0)
    # threshold we are looking for: t
    # flag for iteration
    flag = True

    # 1. calculate the optimum values for b and r
    numberOfRows = 0
    while flag:
        numberOfRows+=1
        # increment from min value until t~(1/b)^(1/r)
        # range (start, stop[, step])
        for r in range(numberOfRows, np.size(sigMatrix,0), numberOfRows):
            b = float(n)/float(r)
            b = math.floor(b)
            base = float(1)/float(b)
            exp = float(1)/float(r)
            # (1/b)^(1/r)
            val = float((base)**(exp))
            #print("b:%d  r:%d  val:%f" % (b, r, val))
            # if (1/b)^(1/r)~t, then break the loop
            # inRange looks for he value to be close to the t that we want as a threshold
            if inRange(val, t):
                flag = False
                break
    b = int(b)
    r = int(r)

    # 2. check if r & b are chosen correctly
    if b*r != len(sigMatrix):
        print('bands * rows = n is not fulfilled: b:%d  r:%d  n:%d' % (b, r, n))

    # 3. get the candidates
    # 3.1 empty list with a row for each doc
    numberOfDocs = sigMatrix.shape[1]
    lshMatrix = []
    for i in range(numberOfDocs):
        lshMatrix.append([])


    # get candidates
    candidates = []

    offset = 0
    for band in range(b):
        # initialize the bucket for this band
        bucket = {}
        # iterate over the documents
        for doc in range(numberOfDocs):
            colList = sigMatrix[:, doc]
            tempList = []
            for row in range(r):
                tempList.append(colList[row + offset])
            key = hash(frozenset(tempList)) % k
            if key in bucket:
                bucket[key] = bucket[key]+ [doc]
            else:
                bucket[key]= [doc]
        # check the bucket similar candidates
        #print(bucket)
        for bucketValues in bucket.values():
            if len(bucketValues) > 1 :
                if bucketValues not in candidates:
                    candidates.append(bucketValues)
        offset += r
    # remove possible subarrays
    candidates = list(eachMasterList(candidates))
    print(candidates)
    # 4. Compare the signature of the candidates and only get the ones with a similarity > t
    # check if the candidate pairs really have similar signatures by using CompareSignature for all pairs
    lhsList = calcLSHList(candidates, sigMatrix, t)


    return lhsList
