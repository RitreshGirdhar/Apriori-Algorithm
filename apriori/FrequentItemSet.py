
# Class FreqItemSet reflecting Single FreqItemSet with support, supportCount, lift, confidence
class FreqItemSet:
    def __init__(self,itemset):
        self.itemset=itemset
        self.supportCount=0
        self.support=0
        self.confidence=0
        self.lift=0

    # Update supportCount
    def updateSupportCount(self,transactions):
        count = 0
        for i in transactions:
            check = all(item in i for item in self.itemset)
            if check is True:
                count = count + 1
        self.supportCount = count
        return

    def getSupportCount(self,itemset,transactions):
        count = 0
        for i in transactions:
            check = all(item in i for item in itemset)
            if check is True:
                count = count + 1
        return count

    # Update support = supportCount/total
    def updateSupport(self,transactions):
        self.support = self.supportCount/ len(transactions)
        return

    # Update confidence = supportCount(x)/supportCount(y). For X->Y
    def updateConfidence(self,x,y,transactions):
        self.confidence = self.getSupportCount(x,transactions) / self.getSupportCount(y,transactions)
        return

    def updateLift(self,x,y,transactions):
        self.lift = self.support / ((self.getSupportCount(x,transactions)/len(transactions))*(self.getSupportCount(y,transactions)/len(transactions)))
        return

    def __hash__(self):
        return hash(self.itemset)

    def __str__(self):
         return "[Frequent Item:{self.itemset}, confidence: {self.confidence}, supportCount: {self.supportCount}, confidence: {self.confidence}]"