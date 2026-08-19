class Node:
    
    def __init__(self):         #Constructor method
        self.Data = ""
        self.Pointer = None     #Pointer references a Node object

    def setData(self, data):
        self.Data = data
        
    def getData(self):
        return self.Data
    
    def setPointer(self, ptr):
        self.Pointer = ptr
        
    def getPointer(self):
        return self.Pointer
    
class LinkedList:
    def __init__(self):         #Initialise method
        self.Start = None       #Start references a Node object

    def IsEmpty(self):
        if self.Start == None:
            return True
        return False

    def AddNode(self, NewData): #add new node to tail of linked list
        newNode = Node() #instantiates a new node object
        newNode.setData(NewData)
    
        if self.IsEmpty():
            self.Start = newNode
        else:
            current = self.Start
            while current.getPointer() != None:
                current = current.getPointer()
            current.setPointer(newNode)
    
    def DeleteNode(self, Data): #delete node storing Data
        if self.IsEmpty():
            return None
        else:
            previous = None
            current = self.Start
            
            while current.getData() != Data and current.getPointer() != None: #assumes there will be a node found
                previous = current
                current = current.getPointer()

            if current.getData() == Data and current == self.Start: #delete first node
                self.Start = current.getPointer()
            elif current.getData() == Data:
                previous.setPointer(current.getPointer())
            else:
                print(Data,": node not found.")

    def CaptureToList(self):
        lst = [] #returns list for marking purpose on Coursemology
        
        if self.IsEmpty():
            return None
        else:
            current = self.Start
            lst.append(current.getData())
            while current.getPointer() != None:
                   current = current.getPointer()
                   lst.append(current.getData())

        return lst

    #The next 4 functions are the algorithms from Tutorial question 3
    def count_nodes(self):
        count = 0
        current = self.Start
        while current is not None:
            count += 1
            current = current.getPointer()
        return count

    def update_data(self, target, new_value):
        current=self.Start
        while current is not None:
            if current.getData() == target:
                current.setData(new_value)
            current= current.getPointer()

    def append_linked_list(self, other):
        if self.Start is None:
            self.Start = other.Start
        else:
            current = self.Start
            while current.getPointer() is not None:
                current = current.getPointer()
            current.setPointer(other.Start)

    def split_linked_list(self):
        count = self.count_nodes()
        if count < 2:
            return "Cannot split less than 2 nodes"
        middle_index = count//2
        previous = None
        current  = self.Start
        for index in range(middle_index):
            previous = current
            current  = current.getPointer()
        previous.setPointer(None)

        newLinkedList = LinkedList()
        newLinkedList.Start = current
        return newLinkedList
    
#Testing code
#===========#

lst = LinkedList()
print(lst.IsEmpty() ==  True)
lst.AddNode("josepshooling@moe.edu.sg")
lst.AddNode("rih2computing@gmail.com")
print(lst.CaptureToList())
print(lst.IsEmpty() == False)
lst.DeleteNode("rih2computing@gmail.com")
lst.DeleteNode("hohoho@gmail.com")
lst.AddNode("sunflowerseed@gmail.com")
lst.AddNode("wateringcan@gmail.com")
print(lst.CaptureToList())
print(lst.count_nodes())
lst.update_data("wateringcan@gmail.com","waterbottle@yahoo.com")
print(lst.CaptureToList())
lst2 = LinkedList()
lst2.AddNode("stargaze@qmail.com")
lst.append_linked_list(lst2)
print(lst.count_nodes())
print(lst.CaptureToList())
newLst = lst.split_linked_list()
print(lst.CaptureToList())
print(newLst.CaptureToList())
