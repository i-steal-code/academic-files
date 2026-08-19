class Node:
    def __init__(self, name='',mark=0,leftP=0,rightP=0):
        self.__Name = name
        self.__Mark = mark
        self.__LeftP = leftP
        self.__RightP = rightP

    def setLeftP(self,ptr):
        self.__LeftP = ptr

    def getLeftP(self):
        return self.__LeftP

    def setRightP(self,ptr):
        self.__RightP = ptr

    def getRightP(self):
        return self.__RightP

    def setName(self,name):
        self.__Name = name

    def getName(self):
        return self.__Name

    def setMark(self,mark):
        self.__Mark = mark

    def getMark(self):
        return self.__Mark

class BST:
    
    def __init__(self,size=7):
        self.__ResultTree = [None]+[Node() for i in range(size)]
        for i in range(1,len(self.__ResultTree)):
            self.__ResultTree[i].setLeftP(i+1)
        self.__ResultTree[size].setLeftP(0) #redundant 
        self.__Root = 0
        self.__NextFree = 1

    def IsEmpty(self):
        return self.__Root == 0

    def IsFull(self):
        return self.__NextFree == 0

    def AddData(self,name,mark):
        #validate name and mark
        if not name.isprintable():
            print("invalid name")
            return None
        if not str(mark).isdigit():
            print("Invalid mark")
            return 
        if self.IsFull():
            print("No free nodes available")
            return
        #since there is free node, let's grab from free list, assign name and mark to the node
        temp = self.__ResultTree[self.__NextFree].getLeftP()
        self.__ResultTree[self.__NextFree].setName(name)
        self.__ResultTree[self.__NextFree].setMark(mark)
        self.__ResultTree[self.__NextFree].setLeftP(0)
        self.__ResultTree[self.__NextFree].setRightP(0)
        #after initialising the new node to be used, we are going to put that node into the bst
        if self.IsEmpty():
            self.__Root = self.__NextFree
        else:
            Current = self.__Root
            LastMove = 'X'
            while Current != 0:
                Previous = Current
                if mark < self.__ResultTree[Current].getMark():
                    LastMove = 'L'
                    Current = self.__ResultTree[Current].getLeftP()
                else:
                    LastMove = 'R'
                    Current = self.__ResultTree[Current].getRightP()
            if LastMove == 'L':
                self.__ResultTree[Previous].setLeftP(self.__NextFree)
            elif LastMove == 'R':
                self.__ResultTree[Previous].setRightP(self.__NextFree)
        self.__NextFree = temp

    def DisplayData(self):
        print("{:^6}|{:^6}|{:^6}|{:^15}|{:^15}".format("Index","Left","Right","Data","Mark"))
        for i in range(1,len(self.__ResultTree)):
            print("{:^6}|{:^6}|{:^6}|{:^15}|{:^15}".format(i, self.__ResultTree[i].getLeftP(),\
                            self.__ResultTree[i].getRightP(),\
                            self.__ResultTree[i].getName(),\
                            self.__ResultTree[i].getMark()))
        print("Root =",self.__Root)
        print("NextFree =",self.__NextFree)

    def GetLowest(self):
        if self.IsEmpty():
            print("No data. Empty tree")
            return
        index = self.__Root
        while self.__ResultTree[index].getLeftP() != 0:
            index = self.__ResultTree[index].getLeftP()
        lowestMark = self.__ResultTree[index].getMark()
        lowestName = self.__ResultTree[index].getName()
        print("{} scored lowest mark with {}.".format(lowestName,lowestMark))

    def InOrder(self, index, rankList):
        if index != 0: #when not null, can traverse further
            self.InOrder(self.__ResultTree[index].getLeftP(), rankList)
            rankList.append((self.__ResultTree[index].getName(),\
                            self.__ResultTree[index].getMark()))#access root node data
            self.InOrder(self.__ResultTree[index].getRightP(), rankList)
        return rankList

    def SearchMoreEqual(self, thisScore): #search for all scores that are >= thisScore
        if self.IsEmpty():
            print("No data. Empty tree")
            return
        index = self.__Root
        rankList = self.InOrder(self.__Root, [])
        for record in rankList:
            if record[1] >= thisScore:
                print("{}, {}".format(rankList[0],rankList[1]))

    def getRoot(self):
        return self.__Root
    
def ConstructBST():
    bst1 = BST(10)
    bst1.AddData("Ahmad Ibrahim",'60')
    bst1.AddData("Victor Lim",'50')
    bst1.AddData("Mary Ho",'80')
    bst1.AddData("Kannan",'75')
    bst1.AddData("Joel Tan",'85')
    bst1.AddData("John Barnes",'35')
    bst1.AddData("Pan Li",'70')
    bst1.AddData("Ray Yeo",'48')
    bst1.DisplayData()
    bst1.GetLowest()
##    ranklist=[]
##    print(bst1.InOrder(bst1.getRoot(),ranklist))
    bst1.SearchMoreEqual(70)

ConstructBST()
