#!/usr/bin/python
import time
import urllib2,json
import httplib,urllib
while True:
    params=urllib.urlencode({'field1':22.6759958,'field2':88.3682527,'field3':20,'field4':464,'key':'WBIGJ0IY2V1BJW40'})
    header={"Content-typZZe":"application/x-www-form-urlencoded","Accept":"text/plain"}
    conn=httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST","/update",params,header)
        response=conn.getresponse()
        print('Datapoint uploaded...')
        data=response.read()
        conn.close()
    except:
        print('Failed...')
    
