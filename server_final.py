#!/usr/bin/python
import time
import webbrowser
from pymongo import MongoClient
from twilio.rest import Client 
import urllib2,json
import httplib,urllib
import subprocess as sp
import random
numbers=range(1000,9999)
#Twilio Credentials
account_sid="ACd90a366ff5022fd855947f76ad092111"
auth_token="d2be14f5dad17085f42b34c4722ab515"
twilio_client=Client(account_sid,auth_token)
#Map Opener
url='file:///home/jun_ishikawa/Desktop/map_display'
#Setup MongoDB
client=MongoClient("mongodb://jun_ishikawa:EUgx3hId7TuJnZeZ@car-e-mainframe-shard-00-00-tppcz.mongodb.net:27017,car-e-mainframe-shard-00-01-tppcz.mongodb.net:27017,car-e-mainframe-shard-00-02-tppcz.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=Car-E-Mainframe-shard-0&authSource=admin")
db=client.database
#Modules
def clear_server():
	comm=raw_input('Warning!All data will be wiped![y/n]:')
	if(comm=='y'):
		try:
			action=db.database.delete_many({})
			print('Action Successful! All data has been wiped from database!')
		except:
			print('Action Unsuccessful!')
	else:
		print('Action aborted!')

def verify_mobile_no(phone_number):
	random_number=random.choice(numbers)
	message=twilio_client.api.account.messages.create(to=phone_number,from_="+13476958859",body=str(random_number))
	code=raw_input('Enter OTP:')
	if(code==random_number):
		print('Phone number verified!')
def create_entry():
	name=raw_input('Input Name:')
	phone_number=raw_input('Input phone number:')
	verify_mobile_no(phone_number)
	car_no=raw_input('Input car number:')
	database={'name':name,'phone number':phone_number,'car number':car_no}
	result=db.database.insert_one(database)
	print('Done!')

while(True):
	command=raw_input('root@nyx>>')
	if(command=='server.clear'):
		clear_server()
	elif(command=='server.input'):
		create_entry()

