#!/usr/bin/python
'''
While editing the code please replace all print statements with the necessary OLED print equivalents.
In the beginning of the program execution cycle please input the boot animation.
use main_integration.txt as a model for creating the program execution cycle.
Necessary library files for the OLED integration to all versions of beaglebone is already included.
'''
import cv2
import time
import json
import httplib, urllib
from multiprocessing import Process
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Image
import ImageDraw
import ImageFont
from time import sleep
import urllib2,json
from twilio.rest import Client
from pymongo import MongoClient
READ_API_KEY='34TIP2BFH1I49FED'
CHANNEL_ID=260939
key1 = '1F908GQOI7BQA9RR'  # Thingspeak channel to update
UID=''
threshold_alchahol=0
threshold_gsr=0
ignition_control_pin=""
#Pins for alchahol and GSR Sensors.
analog_Pin_1="P9_35"
analog_Pin_2="P9_33"
#Security pads have been no pin numbers and number of pads available are completely scalable
pad1=""
pad2=""
pad3=""
pad4=""
GPIO.setup(pad1,GPIO.IN)
GPIO.setup(pad2,GPIO.IN)
GPIO.setup(pad3,GPIO.IN)
GPIO.setup(pad4,GPIO.IN)
GPIO.setup(ignition_control_pin,GPIO.OUT)
#Framing all important modules
def initiate_server_comms():
        while(1):
                conn = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                           % (CHANNEL_ID,READ_API_KEY))
                response = conn.read()
                print "http status code=%s" % (conn.getcode())
                data=json.loads(response)
                x=data['field1']
                z=' '
                conn.close()
def send_warning():
        while True: 
                temp = UID
                params = urllib.urlencode({'field1': temp, 'key':key }) 
                headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
                conn = httplib.HTTPConnection("api.thingspeak.com:80")
                try:
                    conn.request("POST", "/update", params, headers)
                    response = conn.getresponse()
                    print temp
                    print response.status, response.reason
                    data = response.read()
                    conn.close()
                except:
                    print "connection failed"
                break
def security():
        #Please edit the URL given below according to your cluster
        client = MongoClient("mongodb://jun_ishikawa:KHANKIMAGI@car-e-mainframe-shard-00-00-tppcz.mongodb.net:27017,car-e-mainframe-shard-00-01-tppcz.mongodb.net:27017,car-e-mainframe-shard-00-02-tppcz.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=Car-E-Mainframe-shard-0&authSource=admin")
        db=client.database
        print('Initializing security check....')
        key="01001101"#Dummy key.
        car_no="WB069102"
        check = db.database.find_one({'car number': 'DL011303'})
        current_key=check.get('pass code')
        while True:
                val1=GPIO.input(pad1)
                val2=GPIO.input(pad2)
                val3=GPIO.input(pad3)
                val4=GPIO.input(pad4)
                current_key+=val1+val2+val3+val4
                if(len(current_key)==len(key) and current_key!=key):
                        print('Sorry! You entered the wrong key! Try again...')
                        current_key=''
                elif(len(current_key)==len(key) and current_key==key):
                        #Match key with car number from database.
                        print 'Welcome ',check.get('name'),'!'
                        UID=check.get('uid')
                        threshold_gsr=check.get('GSR Threshold')
                        threshold_alchahol=check.get('Alchahol Threshold')


def gsr_alcohol():
        while(True):
                val=ADC.read(analog_Pin_1)
                val2=ADC.read(analog_Pin_2)
                val=int(val*1000)
                val2=int(val2*1000)
                if(val>threshold_gsr or val2>threshold_alchahol):
                        GPIO.output(ignition_control_pin,HIGH)#Disables ignition by turning the ignition lock on.
                        mydata = {}
                        mydata['api_key'] = key1
                        r = requests.delete(URL_delete, data=json.dumps(mydata))
                        send_warning()#Warns serverside of anomaly with particular customer.
                        continue
                elif(val>threshold_gsr and val2>threshold_alchahol):
                        GPIO.output(ignition_control_pin,LOW)
                        break
def camera():
        cascPath = "haarcascade_eye_tree_eyeglasses.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        cap=cv2.VideoCapture(0)
        cap.set(3,320)
        cap.set(4,240)
        key_var=0
        i=0
        counter=0
        #cap.set(cv2.cv.CV_CAP_PROP_FPS, 10)
        while (True):
                gsr_alcohol()
                key_var=0
                i=0
                ret,frame=cap.read()
                if(ret):
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(30, 30),flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
                        for (x, y, w, h) in faces:
                                i+=1
                                print('Looking forward')
                                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                key_var=1
                if(key_var==0 and counter<=4 ):
                        counter+=1
                elif(key_var==0 and counter>4 ):
                        print("You've not been looking forward beyond the permissible time ")
                elif(key_var==1 and counter<=4):
                        counter=0
                elif(key_var==1 and counter>4):
                        counter=0
                if(i<2):
                        print("Not looking forward")
                cv2.imshow('Video', frame)
                k=cv2.waitKey(20)
                if k>=27:
                        break
        cv2.destroyAllWindows()

#Main Code Execution starts from here.

#Play boot animation at the start of the program.

security()#Input the code from user.

gsr_alcohol()#Check if customer is drunk.

#Begin real-time monitoring and parallel/multi-processing.
p1=Process(target=gsr_alcohol)
p1.start()
p2=Process(target=camera)
p2.start()
p1.join()
p2.join()

