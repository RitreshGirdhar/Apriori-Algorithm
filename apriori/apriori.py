import xlrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from FrequentItemSet import FreqItemSet

# return transactions remove null values from each record
def get_transactions(datasetPath):
    wb = pd.read_excel(datasetPath)
    df = pd.DataFrame(wb)

    itemsets = {}
    transactions= []
    for index, row in df.iterrows():
        temp = []
        for i in row:
            if pd.isna(i) == False:
                if(itemsets.get(i)):
                    itemsets.update({i: (itemsets.get(i)+1)})
                else:
                    itemsets.update({i: 1})
                temp.append(i)
        transactions.append(temp)
    return transactions

# Return unique elements of dataset with the number of times items occur
def unique_candidates(transactions):
    itemsets = {}
    for i in transactions:
        for j in i:
            if(itemsets.get(j)):
                itemsets.update({j: (itemsets.get(j)+1)})
            else:
                itemsets.update({j: 1})
    return itemsets

# Divide the dataset into n number of samples. Return dataset transactions by random shuffling
def get_sample_transactions(transactions,number_of_samples):
    avg = len(transactions) / float(number_of_samples)
    out = []
    last = 0.0
    while last < len(transactions):
        out.append(transactions[int(last):int(last + avg)])
        last += avg
    return out

# Return initial combination of unique elements
def inital_candidates(transactions,itemsets,min_support):
    candidates = []
    uniqueMap= {}
    for i in itemsets:
        for j in itemsets:
            if i != j :
                temp = sorted([i,j])
                appendStr = ''.join(temp)
                if appendStr not in uniqueMap:
                    f1 = FreqItemSet(temp)
                    f1.updateSupportCount(transactions)
                    candidates.append(f1)
                    uniqueMap.update({appendStr: 1})

    temp = []
    for i in candidates:
        if i.supportCount > min_support :
            temp.append(i)
    return temp

# combine two list , remove duplicate item
def union(list1,list2):
    temp =  list1 + list(set(list2) - set(list1))
    return sorted(temp)

# print candidates list - used for testing
def print_candidates(candidates):
    for i in candidates:
        print(i.itemset,i.supportCount)

# return frequent itemsets for provided supportCount only and limit iteration with max iteration and
def frequent_itemsets(candidates1,transactions,max_iteration,min_support):
    for x in range(0,max_iteration):
        unique_element = 3+x
        uniqueMap= {}
        nextCandidatesList=[]
        for i in range(0,len(candidates1)):
            for j in range(1,len(candidates1)):
                temp = union(candidates1[i].itemset,candidates1[j].itemset)

                if len(temp) == unique_element:
                    appendStr = ''.join(temp)
                    if appendStr not in uniqueMap:
                        f1 = FreqItemSet(temp)
                        f1.updateSupportCount(transactions)
                        f1.updateSupport(transactions)
                        f1.updateLift(candidates1[i].itemset,list(set(candidates1[j].itemset) - set(candidates1[i].itemset)),transactions)
                        f1.updateConfidence(candidates1[i].itemset,list(set(candidates1[j].itemset) - set(candidates1[i].itemset)),transactions)
                        nextCandidatesList.append(f1)
                        uniqueMap.update({appendStr: 1})

        temp = []
        for i in nextCandidatesList:
            if i.supportCount >= min_support :
                temp.append(i)

        if(len(temp)==0):
            return candidates1

        candidates1=temp
    return candidates1

def main(datasetPath):
        # 1. Load dataset transactions
        transactions = get_transactions(datasetPath)

        # 2. divide the transactions into 100 datasets, random shuffling
        sample_transactions = get_sample_transactions(transactions,10)

        number_of_rules = 0
        samples = []
        rules = []
        output_file = open('output.txt', 'w')
        # 3. iterate each dataset
        for i in range(0,len(sample_transactions)):
            # 4. get unique candidates
            candidates = unique_candidates(sample_transactions[i])
            # 5. get initial candidates set , Support count 3.
            # Considering only single parameter check We could use confidence,lift,support as well
            frequent_itemset = inital_candidates(sample_transactions[i],candidates,3)
            # 6. Get all the frequent_itemsets , max 10 unique_element allowing
            tmp = frequent_itemsets(frequent_itemset,sample_transactions[i],10,3)

            # 7. populating values to generate graph
            number_of_rules = number_of_rules+ len(tmp)
            samples.append(i)
            rules.append(number_of_rules)
            for j in tmp:
                print("item-set",i,j.itemset,j.supportCount,j.support,j.confidence,j.lift)
                output_file.write("item-set {} {} {} {} {} {} \n".format(i,j.itemset,j.supportCount,j.support,j.confidence,j.lift))

        output_file.close()
        plt.plot(rules,samples)
        plt.xlabel('Number of rules')
        plt.ylabel('Iterations')
        plt.title('Grocery Recommendation!')
        plt.show()

# Execute Dataset
main("Dataset.xlsx")