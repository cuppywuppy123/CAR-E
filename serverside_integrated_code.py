#!/usr/bin/python
import time
import webbrowser
from pymongo import MongoClient
import urllib2,json
import httplib, urllib
import subprocess as sp
url = 'file:///home/jun_ishikawa/Desktop/map_display.html'
client = MongoClient("mongodb://jun_ishikawa:KHANKIMAGI@car-e-mainframe-shard-00-00-tppcz.mongodb.net:27017,car-e-mainframe-shard-00-01-tppcz.mongodb.net:27017,car-e-mainframe-shard-00-02-tppcz.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=Car-E-Mainframe-shard-0&authSource=admin")
db=client.database
activation_channel_key='H7DFJE7E5N8ZX2L9'
x=0
def initiate_gps_protocol():
        while(1):
                conn = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                           % (266168,'KCWU33ZC6ZF96NZS'))
                response = conn.read()
                print "http status code=%s" % (conn.getcode())
                data=json.loads(response)
                x=data['field1']
                if(x=='20'):
                	print('Initiating GPS Tracker Systems...')
                	conn.close()
                	break
                else:
                	conn.close()
                	continue

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
def send_engage_signal():
    while True:
    	temp = 10
        key=''
        params = urllib.urlencode({'field1': temp, 'key':activation_channel_key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
        	conn.request("POST", "/update", params, headers)
        	response = conn.getresponse()
        	print 'Communications to all clients enabled...'
        	data = response.read()
        	conn.close()
        except:
        	print "Failed to send engage signal. Contact System Administrator...."
        break
def insert():
	name=raw_input('Please enter the name:')
	carno=input('Please enter the car number:')
	passcode=input('Please enter the passcode:')
	uid=input
	result=db.database.insert_one({'name':name,'car number':carno,'pass code':passcode})
	print('Entry successful!')
while(True):
	sp.call('clear',shell=True)
	print('Welcome to CAR-E Serverside Terminal...')
	print('Enter what you want to to:')
	print('------------------------------------------')
	print('1.Create new entry to database')
	print('2.Open Server')
	print('3.Close Server[Warning:2 way communications will be turned off until you turn on. Not Recommended!]')
	print('4.Listen for requests')
	input_var=input('>>')
	if input_var==1:
		insert()
		time.sleep(4)
	elif input_var==2:
		send_engage_signal()
		time.sleep(4)
	elif input_var==3:
		x=raw_input('[Disengage Confirmation[y/n]:')
		if x=='y':
			send_disengage_signal()
		elif x=='n':
			print('Disengage sequence cancelled...')
		else:
			print('Input could not be processed...[Disengage sequence cancelled]')
		time.sleep(4)
	elif input_var==4:
		print('listening...')
		initiate_gps_protocol()
		webbrowser.open_new(url) # opens in default browser
		alert('grg')
		