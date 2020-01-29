# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 21:26:41 2019

@author: looly
"""

#to implement the Apriori algorithm for finding frequent itemsets with support 
#at least s in a dataset of sales transactions.  
#Support of an itemset is the number of transactions containing the itemset. 

import itertools
from time import time
from rules import generateRules
from collections import defaultdict


def getSupport(items,support_threshold, numberofTransactions):
        #return a dict with {itemset:support}
        right_items = {}
        for item, count in items.items():
            #calculate the support
            s = count/numberofTransactions
            #filter out the item/itemset that don't fulfill the minsupport criteria
            if s >= support_threshold:
               right_items[item] = s
        return right_items
               
def flatten_tuples(tuples):
    #flatten tuple into a set 
    #set makes sure no element is repeated
        return {item for sublist in tuples for item in sublist}

def generateCandidates(path, k_candidates, support_threshold, k):
    #get k-frequent itemsets
    #initialize values
    final_candidates = {}
    candidates =  defaultdict(int)
    numberofTransactions = 0
    if k == 1:
        with open(path, "r") as f:
        #iterate through the dataset
            for line in f:
                #get rid of \n
                line = line.strip()
                #split all items into individual entries in a list
                transaction_line = line.split(" ")
                numberofTransactions += 1 
                #iterate through item and increment by the value by one if item
                # is already in the dict
                for item in transaction_line: 
                    candidates[item] += 1
        # get all candidates that fulfill the support criteria
        final_candidates.update(getSupport(candidates, support_threshold, numberofTransactions))
        print('NUMBER OF CANDIDATES IN C %d: %d' % (k,len(candidates)))
        print('NUMBER OF FREQUENT ITEMS IN L %d: %d' % (k,len(final_candidates))) 
    
    elif k == 2:
        k_candidates = set(k_candidates)
        with open(path, "r") as f:
        #iterate through the dataset
            for line in f:
                #get rid of \n
                line = line.strip()
                #split all items into individual entries in a list and convert it into set
                transaction_line = set(line.split(" "))
                numberofTransactions += 1 
                #get the elements that appear in both k-candidates and transaction-line
                same_candidates = transaction_line.intersection(k_candidates)
                if len(same_candidates) >= k:
                    #get all possible combination of 2-tuples
                    candidatesasTuple= itertools.combinations(sorted(same_candidates), k)
                    #iterate through all k-tuples and increment by the value by one if k-tuple
                    # is already in the dict
                    for itemset in candidatesasTuple:
                        candidates[itemset] +=1
        # get all candidates that fulfill the support criteria
        final_candidates.update(getSupport(candidates, support_threshold, numberofTransactions))
        print('NUMBER OF CANDIDATES IN C %d: %d' % (k,len(candidates)))   
        print('NUMBER OF FREQUENT ITEMS IN L %d: %d' % (k,len(final_candidates))) 
            
    else:
        k_candidates = set(k_candidates)
        #flatten the k-candidates tuple into a set
        k_candidates = flatten_tuples(k_candidates)
        #iterate through the dataset
        with open(path, "r") as f:
            for line in f:
                #get rid of \n
                line = line.strip()
                #split all items into individual entries in a list and convert it into set
                transaction_line = set(line.split(" "))
                numberofTransactions += 1 
                #get the elements that appear in both k-candidates and transaction-line
                same_candidates = transaction_line.intersection(k_candidates)
                if len(same_candidates) >= k:
                    #get all possible combination of k-tuples
                    candidatesasTuple = itertools.combinations(sorted(same_candidates), k)
                    #iterate through all k-tuples and increment by the value by one if k-tuple
                    # is already in the dict
                    for itemset in candidatesasTuple:
                        candidates[itemset] +=1
          
        # get all candidates that fulfill the support criteria            
        final_candidates.update(getSupport(candidates, support_threshold, numberofTransactions))
        print('NUMBER OF CANDIDATES IN C %d: %d' % (k,len(candidates))) 
        print('NUMBER OF FREQUENT ITEMS IN L %d: %d' % (k,len(final_candidates))) 
    return final_candidates
    
    
def findFrequentItems(path, support_threshold):
##get frequent item sets with support above support_threshold
#output is a dict: {count:{itemset:support}} 

    frequentItemSet = {}   
    count = 1
    flag = True
    #count is the number items inside a single set
    while flag: 
        if count == 1:
            #get the singletons
            frequentItemSet[count] = generateCandidates(path, None, support_threshold, count)
        else:
            #enter this fcn if you have more than one item in your set
            #get k-frequent-candidates
            frequentItemSet[count] = generateCandidates(path, frequentItemSet[count-1].keys(), support_threshold,count)
        #test if no more frequent itemsets can be found end while-loop
        if len(frequentItemSet[count]) == 0:
            del(frequentItemSet[count])
            break
        count += 1

    
    return frequentItemSet
    
def apriori(support_threshold,minconf):

    # part 1: get frequent itemsets
    path = "./Dataset/T10I4D100K.dat"
    start = time()
    frequentItems = findFrequentItems(path, support_threshold)
    print(time() - start)
    print('FREQUENT ITEMS:')
    print(frequentItems)
    
    # part 2: generate rules
    start = time()
    rules = generateRules(frequentItems, minconf)
    print(time() - start)
    print('RULES:')
    print(rules)
    

if __name__ == "__main__": 
    
    support_threshold  = input("Enter min-support value, which should be between 0 and 1: ")
    
    if support_threshold  == '':
       support_threshold = 0.01
    else:
        support_threshold  = float(support_threshold)
        
    minconf= input("Enter a min-confidence value, which should be between 0 and 1: ")
    
    if minconf == '':
       minconf = 0.9
    else:
       minconf = float(minconf)
       
    apriori(support_threshold,minconf)
         