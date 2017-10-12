import datetime
import time
from datetime import date
from astral import Astral
import urllib2
import json
from pprint import pprint
#from pyh import *
import sys


def getTimes(city):
	city_name=city
	a = Astral()
	a.solar_depression = 'civil'
	city = a[city_name]
	sun = city.sun(date=date.today(), local=True)
	#print('Latitude: %.02f; Longitude: %.02f\n' % (city.latitude, city.longitude))
#	print (sun)
	print('<h2>Sun and Moon</h2>')
	dawnstr = (str(sun['dawn'])).split(" ",2)[1]
	dawnstr = dawnstr.replace('-04:00',' ')
	print('Dawn:    %s<p>' % dawnstr)
	sunrisestr = (str(sun['sunrise'])).split(" ",2)[1]
	sunrisestr = sunrisestr.replace('-04:00',' ')
	print('Sunrise: %s<p>' % sunrisestr)
	noonstr = (str(sun['noon'])).split(" ",2)[1]
	noonstr = noonstr.replace('-04:00',' ')
	print('Noon:    %s<p>' % noonstr)
	sunsetstr = (str(sun['sunset'])).split(" ",2)[1]
	sunsetstr = sunsetstr.replace('-04:00',' ')
	print('Sunset:  %s<p>' % sunsetstr)
	duskstr = (str(sun['dusk'])).split(" ",2)[1]
	duskstr = duskstr.replace('-04:00',' ')
	print('Dusk:    %s<p>' % duskstr)
#	print('Dusk:    %s' % str(sun['dusk']))
#	print (" ")
	moon = city.moon_phase(date=date.today())
#	print(moon+"/n")
	if moon == 0:
		print("Moon:    New moon")
	elif moon == 7:
		print("Moon:    First quarter")
	elif moon == 14:
		print("Moon:    Full moon")
	else:
		print("Moon:    Last quarter")




def weather():
	f = urllib2.urlopen('http://api.wunderground.com/api/<api_key>/geolookup/conditions/q/MA/Boston.json')
	json_string = f.read()
#	print (json_string)
	parsed_json = json.loads(json_string)
	location = parsed_json['location']['city']
	temp_f = parsed_json['current_observation']['temp_f']
	cond = parsed_json['current_observation']['weather']
	print("<h2>Current Weather</h2>")
	print "Current weather:     %s<p>" % (cond)
	print "Current temperature: %s F<p>" % (temp_f)
	relhum = parsed_json['current_observation']['relative_humidity']
	print "Current relative humidity: %s<p>" % (relhum)
	wind = parsed_json['current_observation']['wind_string']
	print "Current wind:        %s<p>" % (wind)
	pressure = parsed_json['current_observation']['pressure_in']
	pressure_trend = parsed_json['current_observation']['pressure_trend']
	print "Current pressure %s %s<p>" % (pressure, pressure_trend)
	dewpoint = parsed_json['current_observation']['dewpoint_f']
	print "Current dewpoint: %s F<p>" % (dewpoint)
	windchill = parsed_json['current_observation']['windchill_f']
	print "Current windchill: %s F<p>" % (windchill)
	feelslike = parsed_json['current_observation']['feelslike_f']
	print "Feels like: %s F<p>" % (feelslike)
	print
	f.close()
	f = urllib2.urlopen('http://api.wunderground.com/api/<api_key>/geolookup/almanac/q/MA/Boston.json')
	json_string = f.read()
#	print (json_string)
	parsed_json = json.loads(json_string)
	location = parsed_json['location']['city']
	rtemp_low = parsed_json['almanac']['temp_low']['record']['F']
	rtemp_low_year = parsed_json['almanac']['temp_low']['recordyear']
	print "Record low is:  %s F in %s<p>" % (rtemp_low, rtemp_low_year)
	rtemp_high = parsed_json['almanac']['temp_high']['record']['F']
	rtemp_high_year = parsed_json['almanac']['temp_high']['recordyear']
	print "Record high is: %s F in %s<p>" % (rtemp_high, rtemp_high_year)
	print



sys.stdout = open("index.html","w")
print "<html>"
print "<body>"
getTimes("Boston")
print "<p>"
weather()
print "</body>"
print "</html>"
sys.stdout.close()
#print "Boston"
#getTimes("Boston")
#print
#getTimes("Burlington")
#weather()
