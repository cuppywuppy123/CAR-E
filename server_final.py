#!/usr/bin/python
import time
import webbrowser
from pymongo import MongoClient
from twilio.rest import Client 
import urllib2,json
import httplib,urllib
import subprocess as sp
import random
channel_id='291591'
read_api_key='X17XUVVG5C4GM7K8'
html_code="""
<html>
	<style>
		#map
            {
                height: 500px;
                margin: 10px auto;
                width: 800px;
            }
            body {
  font-family: Arial;
  font-size: 15px;
}

#map-canvas {
  height: 400px;
}

#phone-number {
  margin: 5px 0;
  padding: 5px;
  border: 1px solid grey;
}

#phone-number div {
  padding: 5px 0;
}

	</style>
	<body>
  
		<div id="map"></div>
    <div id="map-canvas"></div>
<div id="phone-number"></div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script src="https://maps.googleapis.com/maps/api/js?key= AIzaSyATbeQAjgvzLXAZ3JTU50oQmX7QUmUVTG0 &libraries=places&callback=initMap" async defer></script>
		<script lang="Javascript">
                        var map;
            function initMap() {
            $.getJSON('https://api.thingspeak.com/channels/' + '291591' + '/feed/last.json?api_key=' + 'X17XUVVG5C4GM7K8', function(data) {
              if (navigator.geolocation) {
                try {
                  navigator.geolocation.getCurrentPosition(function(position) {
                  	var myLocation;
                  	var p=22.6759958;
                  	var p1=88.3682527;
                  	
      // get the data point
      p = parseFloat(data.field1);
      p1= parseFloat(data.field2);
      // if there is a data point display it
      

                    //var myLocation = {lat: position.coords.latitude,lng: position.coords.longitude};
                    myLocation = {lat:p,lng:p1}
                    setPos(myLocation);	
                  });
                } catch (err) {
                  var myLocation = {lat: 22.6759958,lng: 88.3682527};
                  setPos(myLocation);
                }
              } else {
                var myLocation = {
                  lat: 23.8701334,
                  lng: 90.2713944
                };
                setPos(myLocation);
              }
               });
            }

            function setPos(myLocation) {
              map = new google.maps.Map(document.getElementById('map'), {
                center: myLocation,
                zoom: 10
              });

              var service = new google.maps.places.PlacesService(map);
              service.nearbySearch({
                location: myLocation,
                radius: 4000,
                types: ['hospital']
              }, processResults);

            }

            function processResults(results, status, pagination) {
              if (status !== google.maps.places.PlacesServiceStatus.OK) {
                return;
              } else {
                createMarkers(results);

              }
            }

            function createMarkers(places) {
              var bounds = new google.maps.LatLngBounds();
              var placesList = document.getElementById('places');
              var val_hum='';
              var val_num='';
              for (var i = 0, place; place = places[i]; i++) {
                var image = {
                  url: place.icon,
                  size: new google.maps.Size(71, 71),
                  origin: new google.maps.Point(0, 0),
                  anchor: new google.maps.Point(17, 34),
                  scaledSize: new google.maps.Size(25, 25)
                };
                val_hum=place.place_id;
                val_num=place.name;


                var marker = new google.maps.Marker({
                  map: map,
                  icon: image,
                  title: place.name,
                  animation: google.maps.Animation.DROP,
                  position: place.geometry.location
                });

                bounds.extend(place.geometry.location);
              }
var service = new google.maps.places.PlacesService(map);

  service.getDetails({
    placeId: val_hum
  }, function(place, status) {
    if (status === google.maps.places.PlacesServiceStatus.OK) {

      console.log(place);

      // Create marker
      var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location
      });

      // Center map on place location
      map.setCenter(place.geometry.location);

      // Get DIV element to display opening hours
      var phoneNumberDiv = document.getElementById("phone-number");

      // Create DIV element and append to opening_hours_div
      var content = document.createElement('div');
      content.innerHTML = 'Name: ' + place.name + '<br>';
      content.innerHTML += 'Formatted phone number: ' + place.formatted_phone_number + '<br>';
      content.innerHTML += 'International phone number: ' + place.international_phone_number;

      phoneNumberDiv.appendChild(content);
    }
  });

              map.fitBounds(bounds);

            }

            </script>
            
            
	</body>
  </html>
  """
filename=""
numbers=range(1000,9999)
account_numbers=range(100,999)
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
	while(True):
		code=raw_input('Enter OTP:')
		if(int(code)==random_number):
			print('Phone number verified!')
			break
		else:
			print('Wrong input! Enter again...')
			continue
def send_signal(phone_number,w,x,car):
	message=twilio_client.api.account.messages.create(to=phone_number,from_="+13476958859",body=car+" is located at "+str(w)+","+str(x))
def create_entry():
	account_number=random.choice(account_numbers)
	name=raw_input('Input Name:')
	phone_number=raw_input('Input phone number:')
	verify_mobile_no(phone_number)
	car_no=raw_input('Input car number:')
	database={'name':name,'phone number':phone_number,'car number':car_no,'account number':str(account_number)}
	filename=str(account_number)+'.html'
	print('Account number:')
	print(account_number)
	f=open(filename,'w')
	f.write(html_code)
	f.close()
	result=db.database.insert_one(database)
	print('Done!')
def trigger_event_action_listener():
	while(True):
		val=0
		conn=urllib2.urlopen("https://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
					%(channel_id,read_api_key))
		response=conn.read()
		print "http status code=%s" % (conn.getcode())
		data=json.loads(response)
		w=data['field1']
		x=data['field2']
		y=data['field3']
		z=data['field4']
		if(x!=0 and y!=0):
			print('Initiating GPS Tracker Systems...')
			if(y!=-999):
				url = 'file:///home/jun/Desktop/CAR-E/'+z+'.html'
				r=db.database.find_one({'account number':z})
				phone_no=r.get('phone number')
				car_no=r.get('car number')
				#print(phone_no)
				#print(car_no)
				send_signal(phone_no,w,x,car_no)
				webbrowser.open_new(url)
			conn.close()
			break
		else:
			conn.close()
			print('Failed to contact GPS! Retrying...')
			continue
while(True):
	command=raw_input('root@nyx>>')
	if(command=='server.clear'):
		clear_server()
	elif(command=='server.input'):
		create_entry()
	elif(command=='server.listen'):
		trigger_event_action_listener()
