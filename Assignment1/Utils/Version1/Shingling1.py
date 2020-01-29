# A class Shingling that constructs k–shingles of a given length k (e.g., 10) from a given document, 
#computes a hash value for each unique shingle, and represents the document in the form of an ordered set of its hashed k-shingles.

import mmh3
import itertools

path = "./DataSet/articles_10.txt"

def shingling(path,k):
    #number of documents
    numDoc = 10
    #dictionary to map the shingles to their document
    docsAsShingleSets = {}
    #shingle size
    # Open the data file
    
    with open(path, "r") as f:
         
        for i in range(0, numDoc):
     
            #reading each line and split the words by their space
            for line in f:
    
                words = line.split(" ") 
                #saving the ID of the 10 documents 
                ID = words[0] 
                #deleting the documents ID
                del words[0]
                # keeping the 9-shingles
                #advantage of sets is that the shingles will only appear once
                shinglesWords = set()
                # keeping the hashed shingles
                shinglesInts = set()
                #put all the words together without space
                newline = "".join(words)
                #to count the number of shingles
                numShingles = 0
                for index in range(0, len(newline)):
                    #extracting the k-shingles
                    shingle = newline[index:index+k]
                    
                    if shingle not in shinglesWords and len(shingle) == k:
                        numShingles += 1
                        shinglesWords.add(shingle)
                        #hashing the shingles
                        crc = mmh3.hash(shingle)

                        if crc not in shinglesInts:
                            shinglesInts.add(crc)
                docsAsShingleSets[ID] = shinglesInts
                
    IDs = list(docsAsShingleSets.keys())

    return IDs, docsAsShingleSets
    
    
def jaccard (IDs,docsAsShingleSets,threshold):
    
    Jaccard_Similarity = {}
    similar_items =[]
    
    for subset in itertools.combinations(IDs,2):
        Jaccard_Similarity[subset] = len(docsAsShingleSets[subset[0]].intersection(docsAsShingleSets[subset[1]])) / len(docsAsShingleSets[subset[0]].union(docsAsShingleSets[subset[1]]))
        if Jaccard_Similarity[subset] > threshold:
            similar_items.append((subset, Jaccard_Similarity[subset]))
 
    
    return similar_items
    
    

    
    

    






  
            
        

        
    
    

        