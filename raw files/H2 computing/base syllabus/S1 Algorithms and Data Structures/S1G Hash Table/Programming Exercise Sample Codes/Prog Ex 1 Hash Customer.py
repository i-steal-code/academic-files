size = 9 # Max capacity of hash table

def hashfunction(data):
    total = 0
    for i in range(len(data)):
        total = total + ord(data[i])
    hashValue = total % size
    return hashValue

def CreateHashTable(): # Initialise hash table with size given
    hashTable = []
    for i in range(size):
        hashTable.append(['',''])
    return hashTable

def rehash(hashCode):
    return (hashCode+1)%size  #step size for linear probing is 1

def AddRecord(filename, hashTable):
    file = open(filename, 'r')
    for line in file:
        Customer_ID, Customer_Name = line.strip().split(',')
        hashCode = hashfunction(Customer_ID) # Find the hash code using hash function
        #store the data (key-value) in the hash table
        if len(hashTable[hashCode][0]) == 0:   # Compare the key
            hashTable[hashCode] = [Customer_ID, Customer_Name]
        else: # Collision handling
            nextSlot = rehash(hashCode) #find the next slot
            while len(hashTable[nextSlot][0]) != 0: #why keep checking ?
                nextSlot = rehash(nextSlot) #find next slot again, is this infinite loop?
                if nextSlot == hashCode: #completed one round of array
                    print("No more space to add new record",Customer_ID)
                    return hashTable
            hashTable[nextSlot] = [Customer_ID, Customer_Name]
    file.close()
    return hashTable

def Search(customerID, hashTable):
    hashCode = hashfunction(customerID) # Find the hash code using hash function
    if hashTable[hashCode][0] == customerID: #customerID found!
        return hashCode
    #not found at initial hashCode!
    nextSlot = rehash(hashCode) #find the next slot
    while (hashTable[nextSlot][0] != customerID) and (nextSlot != hashCode):
        nextSlot = rehash(nextSlot) #find the next slot
    if hashTable[nextSlot][0] == customerID: #found!
        return hashCode
    return -1 #not found

def Delete(customerID, hashTable):
    hashCode = Search(customerID,hashTable) # Find the hash code using hash function
    if hashCode != -1: #found the key in the hashTable
        deleted = hashTable[hashCode]
        hashTable[hashCode] = ["***","***"] # *** denotes deleted data
        return deleted, hashTable
    print(customerID,"not found in hashTable")
    return None, hashTable

def display(hashTable):
    print("{:^5}|{:^10}|{:<15}".format("Index", "CustomerID", "CustomerName"))
    for i in range(len(hashTable)):
        print("{:^5}|{:^10}|{:<15}".format(i, hashTable[i][0], hashTable[i][1]))

ht1 = CreateHashTable()
ht1 = AddRecord("customers.txt", ht1)
display(ht1)
print(Search("A5RD",ht1))
deletedData, ht1 = Delete("A5RD",ht1)
print(deletedData)
display(ht1)
##print(hashfunction("A5RD")) #7
##print(hashfunction("B7MF")) #7
##print(hashfunction("R2YJ")) #7
##print(hashfunction("J6TR")) #6
##print(hashfunction("G4QB")) #0



    
