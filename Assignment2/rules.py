#Solve the second sub-problem, i.e., develop and implement an algorithm for generating association rules between frequent itemsets discovered by using the Apriori algorithm
# in a dataset of sales transactions. The rules must have support at least s and confidence at least c, where s and c are given as input parameters.
# conf (ab -> cd) = supp(abcd) / supp(ab)
import itertools

def generateRules(itemsets, minconf):
    count = 0
    rules = []
    # loop over the outer keys and ignore singletons
    for k in list(itemsets.keys())[1:]:
        # for each frequent k-itemset fk, k>=2 do
        for frequent in itemsets[k]:
            m = 1
            consequents = frequent
            k = len(frequent)
            while m < k:
                hm_plus_1 = list()
                for rightSide in consequents:
                    rightSide2 = set()
                    if isinstance(rightSide, str):
                        rightSide2.add(rightSide)
                    else:
                        for item in rightSide:
                            if type(item) is set:
                                rightSide2.update(item)
                            else:
                                rightSide2.add(item)
                    leftSide = (set(frequent).difference(rightSide2))
                    if len(leftSide) == 1:
                        leftSide = leftSide.pop()
                        conf = itemsets[k].get(frequent) / itemsets[1].get(leftSide)
                    else:
                        leftSide = tuple(sorted(leftSide))
                        keyleft = len(leftSide)
                        conf = itemsets[k].get(frequent) / itemsets[keyleft].get(leftSide)
                    # if conf >=mincinf then
                    if conf >= minconf:
                        # output the rule
                        rules.append((leftSide, rightSide2, conf))
                        count +=1
                        for element in rightSide2:
                            if element not in hm_plus_1:
                                hm_plus_1.append(element)
                hm_plus_1 = list(itertools.combinations(hm_plus_1, m + 1))
                if not hm_plus_1:
                    break
                m = m + 1
                consequents = hm_plus_1
    print('NUMBER OF RULES: %d' % (count))
    return rules





