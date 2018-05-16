import geocoder

g = geocoder.ip('me')
print "City : ", g.city
print "Country : ", g.country
print "State : ", g.state
print "Latitude Longitude : ", g.latlng

import requests

r = requests.get('https://api.ipdata.co', verify=False)
print r.content
r = r.json()
print "Country : ", r['country_name']
print "Latitude : ", r['latitude']
print "Longitude : ", r['longitude']

str = "haaia"
if 'a' in str: print str.replace('a','',1)
print str
l =['a','h','g']
if 'h' in l: print "jhgvh"
else: print ":("