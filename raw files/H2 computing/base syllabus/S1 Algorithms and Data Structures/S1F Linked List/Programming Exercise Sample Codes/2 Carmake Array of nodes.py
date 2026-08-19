#Code for 2(a) and 2(b) are shown here

class Node:
    def __init__(self, data='nothing', ptr=-1):
        self.__name = data #initialise to empty string
        self.__pointer = ptr  #initialise to -1 (null)

    def setName(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    def setPointer(self, ptr):
        self.__pointer = ptr

    def getPointer(self):
        return self.__pointer

class LinkedList:
    def __init__(self, size=8):
        self.__Make=[Node() for i in range(size)]
        self.__Start = -1 #initialise to -1(null)
        self.__NextFree = 0 #initialise to first index
        for i in range(size-1):
            self.__Make[i].setPointer(i+1)

    def Insert(self,item):
        if self.__NextFree == -1:
            print("No free node available")
            return
        self.__Make[self.__NextFree].setName(item)
        if self.__Start == -1: #insert into empty linked list
            temp = self.__Make[self.__NextFree].getPointer()
            self.__Make[self.__NextFree].setPointer(-1)
            self.__Start = self.__NextFree
            self.__NextFree = temp
        else:
            previous = -1
            current  = self.__Start
            while current != -1: #not null
                if item < self.__Make[current].getName():
                    break
                previous = current
                current = self.__Make[current].getPointer()
            if previous == -1: #insert as first node
                temp = self.__Make[self.__NextFree].getPointer()
                self.__Make[self.__NextFree].setPointer(self.__Start)
                self.__Start = self.__NextFree
                self.__NextFree = temp
            else:  #store between previous and current
                temp = self.__Make[self.__NextFree].getPointer()
                self.__Make[self.__NextFree].setPointer(current)
                self.__Make[previous].setPointer(self.__NextFree)
                self.__NextFree = temp

    def Delete(self,item):
        if self.__Start == -1:
            print("List is empty")
            return
        previous = -1
        current  = self.__Start
        while current != -1:
            if item == self.__Make[current].getName():
                break
            previous = current
            current = self.__Make[current].getPointer()
        if current == -1:
            print("Node not found")
            return
        if previous == -1:
            temp = self.__NextFree
            self.__NextFree = current
            self.__Start = self.__Make[current].getPointer()
            self.__Make[current].setPointer(temp)
        else:
            temp = self.__NextFree
            self.__NextFree = current
            self.__Make[previous].setPointer(self.__Make[current].getPointer())
            self.__Make[current].setPointer(temp)

    def Search(self,item):
        pass

    def Display(self):
        print("{:^5}|{:<10}|{:^5}".format("node","name","pointer"))
        for i in range(len(self.__Make)):
            print("{:^5}|{:<10}|{:^5}".format(i, self.__Make[i].getName(), self.__Make[i].getPointer()))
        print("Start =",self.__Start)
        print("NextFree =",self.__NextFree)

#Testing code
#============
carMake=LinkedList()
carMake.Insert("Mazda")
carMake.Insert("Honda")
carMake.Delete("Mazda")
carMake.Insert("Toyota")
carMake.Insert("Nissan")
carMake.Insert("BMW")
carMake.Insert("Kia")
carMake.Insert("Hyundai")
carMake.Insert("VolksWagen")
carMake.Insert("Mercedes")
carMake.Display()

#You need to complete the code for 2(c) to 2(f) 
