import pymongo, csv, json

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['database_db']
studb = db['student']
latedb = db['late']
studb.delete_many({})
latedb.delete_many({})
print("successfully connected to mongoclient")

with open('STUDENT.csv') as file:
    reader = csv.reader(file)
    #fields
    f = next(reader)
    for row in reader:
        record = dict(zip(f,row))
        studb.insert_one(record)

with open('LATE.csv') as file:
    reader = csv.reader(file)
    #headers
    h = next(reader)
    for row in reader:
        latedb.insert_one(dict(zip(h,row)))
print("successfully inserted all records")
query = input("key in class to pull up list of students names")
pipeline = [
    {"$match": {"Class_Group": query}},
    {"$lookup":{
        "from": "late",
        "localField": "Student_ID",
        "foreignField": "Student_ID",
        "as": "late_records"}},
    {"$match": {"late_records": {"$ne": []}}}
]
for result in studb.aggregate(pipeline):
    print(result[f[1]])
client.close()
