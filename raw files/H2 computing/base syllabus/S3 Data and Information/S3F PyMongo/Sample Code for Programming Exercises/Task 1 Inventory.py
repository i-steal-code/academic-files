def task1_1():

    def display(collection,result): # parameters are collection and result
        for doc in result:
            print(doc)
        print(collection.count_documents({}))

    import pymongo

    client = pymongo.MongoClient("localhost",27017)
    print(client.list_database_names())
##    print("Removing OUTLETS database......")
    db = client['OUTLETS']
    coll = client['OUTLETS']['GEM']
    print(client['OUTLETS'].list_collection_names())
    #    client.drop_database("OUTLETS")
    coll.delete_many({}) #delete all documents in GEM
#    print("After removing GEM database:",db.list_collection_names())
    result = coll.find({})
    display(coll,result)	


    file = open("INVENTORY_SERIAL.txt",'r')
    for line in file:
        parts = line.strip().split('\t')
        coll.insert_one({"Serial_No":parts[0], "Name":parts[1],
                         "Type":parts[2], "Purchase_price":parts[3],
                         "Selling_price":parts[4], "Quantity":parts[5]})
    file.close()
    result = coll.find({},{"_id":0})
    display(coll,result)



    client.close()

def task1_2():
    import pymongo
    client = pymongo.MongoClient("localhost",27017)
    coll = client["OUTLETS"]["GEM"]
    result = coll.find({})
    error_doc = [] # Store all the documents with errors

    def check_serial(number):
        if len(number) != 4 or not number[0].isdigit() or \
        not number[1:3].isalpha() or not number[3].isdigit():
            return False
        return True

    def check_name(name):
        for char in name:
            if not char.isalpha() and not char.isspace() and not char.isdigit():
                return False
        return True

    for doc in result:
        if not doc["Quantity"].isdigit():
            error_doc.append(doc)
            coll.delete_one(doc)
        elif not check_serial(doc["Serial_No"]):
            error_doc.append(doc)
            coll.delete_one(doc)
        elif not check_name(doc["Name"]):
            error_doc.append(doc)
            coll.delete_one(doc)

    print(error_doc)
    print(len(error_doc))

    client.close()
