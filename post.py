#!/usr/bin/python
import time
import urllib2,json
import httplib,urllib
while True:
    temp=10
    params=urllib.urlencode({'field1':temp,'key':'1F908GQOI7BQA9RR'})
    conn=httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST","/update",params,headers)
        response=conn.getresponse()
        print('Datapoint uploaded...')
        data=response.read()
        conn.close()
    except:
        print('Failed...')
    
