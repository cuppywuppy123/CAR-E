from pymongo import MongoClient
# Connect to the MongoDB, change the connection string per your MongoDB environment
client = MongoClient("mongodb://jun_ishikawa:KHANKIMAGI@car-e-mainframe-shard-00-00-tppcz.mongodb.net:27017,car-e-mainframe-shard-00-01-tppcz.mongodb.net:27017,car-e-mainframe-shard-00-02-tppcz.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=Car-E-Mainframe-shard-0&authSource=admin")
# Set the db object to point to the business database
db=client.database
# Showcasing the count() method of find, count the total number of 5 ratings 
print('Checking if a given key is valid or not')
checker = db.database.find({'car number': 'DL012201', 'pass code': '110011'}).count()
check2 = db.database.find_one({'car number': 'DL012201'})
print(checker)
if checker==1:
	name_to_be_displayed=check2.get('name')
	print 'Welcome ',name_to_be_displayed,'!'
