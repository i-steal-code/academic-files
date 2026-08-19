class BookRec():

    def __init__(self, ID=None, title=None):
        self.__BookID = str(ID)
        self.__Title  = str(title)
        self.__Pointer = None #pointer

    def GetBookID(self):
        return self.__BookID
 
    def GetTitle(self):
        return self.__Title
 
    def GetPointer(self):
        return self.__Pointer

    def SetBookID(self, ID):
        self.__BookID = str(ID)

    def SetTitle(self, title):
        self.__BookID = str(ID)

    def SetPointer(self, pointer):
        self.__Pointer = pointer

class LinkedList():
    def __init__(self): #Initialise method, constructor
        self.__Start = None

    def __str__(self): #DisplayLinkedList method, return value is displayed by built-in print() function
        output = '' #empty string
        temp = self.__Start
        i = 1
        while temp is not None:
            output += "{0}|{1}|{2}| -> ".format(i,temp.GetBookID(),temp.GetTitle())
            temp = temp.GetPointer()
            i += 1      #increment i
        output += " None"
        return output   #return 'output' for display

    def DisplayLinkedList(self): #DisplayLinkedList method, return value is displayed 
        output = '' #empty string
        temp = self.__Start
        i = 1
        while temp is not None:
            output += "{0}|{1}|{2}| -> ".format(i,temp.GetBookID(),temp.GetTitle())
            temp = temp.GetPointer()
            i += 1      #increment i
        output += " None"
        print(output)   #return 'output' for display

    def GetStart(self):
        return self.__Start

    def IsEmpty(self):
        return self.__Start == None

    def AddNode(self, ID, title):
        NewNode=BookRec(ID, title) #create an instance of NewNode

        if self.IsEmpty():  #add into empty linked list
            self.__Start = NewNode
        else:     #add as first node of non-empty linked list
            temp = self.__Start
            self.__Start = NewNode
            NewNode.SetPointer(temp)

    def DeleteNode(self, ID):
        if self.__Start is not None:
            prev = None
            current = self.__Start
            while current.GetBookID() != ID and current.GetPointer() is not None:
                prev = current
                current = current.GetPointer()

            if prev is None:
                if self.__Start.GetBookID() == ID:
                    self.__Start = current.GetPointer()
            elif current.GetBookID() == ID:
                prev.SetPointer(current.GetPointer())

    def SearchNode(self, ID): #check if data already exists in linked list
        current = self.__Start
        while current is not None:  #traverse linked list till end
            if current.GetBookID() == ID: #check for data
                return True
            current = current.GetPointer() #change pointer to point to next node
        return False

class HashTable():
    def __init__(self, size=17): #Initialise, constructor
        self.__Size = size #number of slots
        self.__Slots = [LinkedList() for i in range(self.__Size)]

    def Hash(self,ID):
        total=0
        for char in ID: #total up each ASCII character
            total=total+ord(char)
        K=total #total ASCII value
        A = K%(self.__Size)+1 #calculate address
        return A

    def Display(self):
        for i in range(self.__Size):
            print("{:^4}|".format(i+1),end='')
            self.__Slots[i].DisplayLinkedList()

    def Put(self,ID,title):
        hashCode = self.Hash(ID)
        thisList = self.__Slots[hashCode] #assign thisList to the hashed index
        thisList.AddNode(ID,title)

    def Remove(self,ID):
        hashCode = self.Hash(ID)
        thisList = self.__Slots[hashCode]
        if thisList.SearchNode(ID) is True:
            thisList.DeleteNode(ID)

    def Search(self,ID):
        hashCode = self.Hash(ID)
        thisList = self.__Slots[hashCode]
        return thisList.SearchNode(ID)

def main():
    h=HashTable(17)
    h.Put("CS733","Basic algorithms")
    h.Put("AB944","Master Computing")
    h.Put("KS293","Data structures")
    h.Put("BK232","Programming exercises")
    h.Put("PK199","Testing Python")
    h.Display()
    print(h.Search("PK199"))
##    h.Remove("CS733")
##    h.Remove("BK232")
##    h.Display()
##    print(h.Search("KS293"))

if __name__ == "__main__":
    main()
