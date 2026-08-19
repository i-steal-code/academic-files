global NullPointer, RootPointer, FreePtr, Tree
NullPointer = 0

class TreeNode:
    def __init__(self,data='',lPtr=0,rPtr=0):
        self.__Data = data
        self.__LeftPointer = lPtr
        self.__RightPointer = rPtr
    def setData(self,data):
        self.__Data = data
    def setLeftPointer(self,ptr):
        self.__LeftPointer = ptr
    def setRightPointer(self,ptr):
        self.__RightPointer = ptr
    def getData(self):
        return self.__Data
    def getLeftPointer(self):
        return self.__LeftPointer
    def getRightPointer(self):
        return self.__RightPointer

Tree = [None] + [TreeNode() for i in range(7)]

def InitialiseTree():
    global NullPointer, RootPointer, FreePtr, Tree
    RootPointer = NullPointer
    FreePtr = 1
    Index = 1
    while Index < 7:
        Tree[Index].setLeftPointer(Index+1)
        Index += 1
    Tree[7].setLeftPointer(NullPointer)

def DisplayTree():
    global NullPointer, RootPointer, FreePtr, Tree
    print("{:^5}|{:^10}|{:^5}|{:^5}".format("Index","Data","Left","Right"))
    for i in range(1, len(Tree)):
        print("{:^5}|{:^10}|{:^5}|{:^5}".format(i,Tree[i].getData(),\
                                Tree[i].getLeftPointer(),
                                Tree[i].getRightPointer()))
    print("RootPointer=",RootPointer)
    print("FreePtr=",FreePtr)

def FindNode(SearchItem):
    global NullPointer, RootPointer, FreePtr, Tree
    current = RootPointer
    while current != NullPointer and Tree[current].getData() != SearchItem:
        if SearchItem < Tree[current].getData():
            current = Tree[current].getLeftPointer()
        else:
            current = Tree[current].getRightPointer()
    if current == NullPointer:
        return f"Cannot find {SearchItem}"
    return current #index of the array

def InsertNode(Newitem):
    global NullPointer, RootPointer, FreePtr, Tree
    if FreePtr != NullPointer: #free node is available
        NewNodePtr = FreePtr
        FreePtr = Tree[FreePtr].getLeftPointer()
        Tree[NewNodePtr].setData(Newitem)
        Tree[NewNodePtr].setLeftPointer(NullPointer)
        Tree[NewNodePtr].setRightPointer(NullPointer)

        if RootPointer == NullPointer:
            RootPointer = NewNodePtr
        else:
            current = RootPointer
            while current != NullPointer:
                previous = current
                if Newitem < Tree[current].getData():
                    TurnedLeft = True
                    current = Tree[current].getLeftPointer()
                else:
                    TurnedLeft = False
                    current = Tree[current].getRightPointer()
            if TurnedLeft:
                Tree[previous].setLeftPointer(NewNodePtr)
            else:
                Tree[previous].setRightPointer(NewNodePtr)
    else:
        print("No free nodes available")

InitialiseTree()
InsertNode("HHH")
InsertNode("III")
InsertNode("JJJ")
InsertNode("AAA")
InsertNode("BBB")
InsertNode("CCC")
InsertNode("DDD")
InsertNode("EEE")
InsertNode("FFF")
InsertNode("GGG")

DisplayTree()
print(FindNode("AAA"))
