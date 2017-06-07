#!/usr/bin/python
from pymongo import MongoClient
import urllib2,json
client = MongoClient("mongodb://jun_ishikawa:KHANKIMAGI@car-e-mainframe-shard-00-00-tppcz.mongodb.net:27017,car-e-mainframe-shard-00-01-tppcz.mongodb.net:27017,car-e-mainframe-shard-00-02-tppcz.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=Car-E-Mainframe-shard-0&authSource=admin")
db=client.database
activation_channel_key=''
def send_disengage_signal():
    while True:
    	temp = 20
        key=''
        params = urllib.urlencode({'field1': temp, 'key':activation_channel_key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
        	conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print 'Communications to all clients disabled...'
            data = response.read()
            conn.close()
        except:
        	print "Failed to send disengage signal. Contact System Administrator...."
        break
def insert():
	name=input('Please enter the name:')
	carno=input('Please enter the car number:')
	passcode=input('Please enter the passcode:')
	result=db.database.insert_one({'name':name,'car number':carno,'pass code':passcode})
	print('Entry successful!')
while(True):
	print('Welcome to CAR-E Serverside Terminal...')
	print('Enter what you want to to:')
	print('------------------------------------------')
	print('1.Create new entry to database')
	print('2.Open Server [Warning:You cannot do other operations once this is turned on.]')
	print('3.Close Server[Warning:2 way communications will be turned off until you turn on. Not Recommended!')
	input_var=input('Listening:')
	if input_var==1:
		insert()
	elif input_var==2:
		#Engage signal.
	elif input_var==3:
		x=input('[Disengage Confirmation[y/n]:')
		if x=='y':
			send_disengage_signal()
		elif x=='n':
			print('Disengage sequence cancelled...')
		else:
			print('Input could not be processed...[Disengage sequence cancelled]')


