#Code the program to initialize both arrays and pointers.
size = 10

Data = [None]+["" for i in range(size)]
Ptr = [None]+[0 for i in range(size)]

for i in range (1,size):
    Ptr[i] = i + 1

Start = 0    #initial value
NextFree = 1 #initial value

#Code procedures to insert a new data into the linked list and delete a data from the linked list.

def InsertRear(data):
    global Start, NextFree
        
    if NextFree == 0:       #linked list full
        print("No free node is available")
        return None

    Data[NextFree] = data

    if Start == 0:          #empty linked list
        Start = NextFree
        NextFree = Ptr[NextFree]
        Ptr[Start] = 0
    else:
        current = Start
        while Ptr[current] != 0: #traverses linked list to locate tail node
            current = Ptr[current]
        temp = Ptr[NextFree]
        Ptr[current] = NextFree
        Ptr[NextFree] = 0
        NextFree = temp

def InsertFront(data):
    global Start, NextFree

    if NextFree == 0:       #linked list full
        print("No free node is available")
        return None

    Data[NextFree] = data

    if Start == 0:  #empty linked list
        Start = NextFree
        NextFree = Ptr[NextFree]
        Ptr[Start] = 0
    else:
        
        Temp = Ptr[NextFree]
        Ptr[NextFree] = Start
        Start = NextFree
        NextFree = Temp
    
def DeleteItem(data): #delete node with surname
    global Start, NextFree
    
    if Start == 0:                          #empty list
        print("No data in linked list!")
        return None
    else:
        current = Start
        while True:
            if Data[current] == data: #assumes there is node with the required data
                break
            previous = current
            current = Ptr[current]

        if current == Start: #first node removed
            temp = NextFree
            Start = Ptr[current]
            NextFree = current
            Ptr[NextFree] = temp
        else:                  #current node removed
            temp = NextFree
            Ptr[previous] = Ptr[current]
            NextFree = current
            Ptr[NextFree] = temp

def Display(Data,Ptr):  #display linked list in table form
    for i in range(1, len(Data)):
        print("{:<5}|{:<7}|{:<7}".format(i, Data[i], Ptr[i]))

#Testing code
#============

def test1():
    s = Start
    nf = NextFree
    print("Initial Start=",s,"\nInitial NextFree=",nf)

    InsertRear("Liu")
    InsertRear("Wong")
    InsertRear("Sandhu")
    Display(Data,Ptr)
    s1 = Start
    nf1 = NextFree
    print("Start",s1,"\nNextFree",nf1)

def test2():
    print("Initial Start =",Start)
    print("Initial NextFree =", NextFree)
    InsertFront("apple")
    InsertFront("pear")
    Display(Data,Ptr)
    print("Final Start =",Start)
    print("Final NextFree =", NextFree)
