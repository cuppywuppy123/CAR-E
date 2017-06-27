from pymongo import MongoClient
#Step 1: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient("mongodb://jun_ishikawa:EUgx3hId7TuJnZeZ@car-e-mainframe-shard-00-00-tppcz.mongodb.net:27017,car-e-mainframe-shard-00-01-tppcz.mongodb.net:27017,car-e-mainframe-shard-00-02-tppcz.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=Car-E-Mainframe-shard-0&authSource=admin")
db=client.database
#Step 2: Create sample data
names = ['Avijoy Haldar','Rajat Saxena','Divyansh Agrawal']
car_number = ['WB069102','DL011303','TN021011']
passkey = ['010111', '100101', '111001']
for x in xrange(0, 3):
    database = {
        'name' : names[x],'car number' : car_number[x],'pass code' : passkey[x] 
    }
    #Step 3: Insert business object directly into MongoDB via isnert_one
    result=db.database.insert_one(database)
    #Step 4: Print to the console the ObjectID of the new document
    print('Created {0} of 3 as {1}'.format(x,result.inserted_id))
#Step 5: Tell us that you are done
insert_result=db.database.insert_one({'name' : 'Zayn Malik','car number' : 'DL012201','pass code':'110011'})
print('finished creating 3 user records')