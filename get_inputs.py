from tzwhere import tzwhere
from geopy import geocoders
import pytz
import datetime as dt



def get_inputs(args):
	'''
	A function that returns command line inputs, returns custom inputs, or returns default inputs
	Inputs 
		args: command line arguments
	Outputs
		date_time_local: Aware datetime obj (has timezone) of time at location you query
		LA: latitude in decimal format
		LO: longitude in decimal format
		city
	'''

	# if there is city input, it will override LA, LO input
	if args.city == None:
		LA = -1.286389 #Latitude, decimal degrees -90 to 90
		LO = 36.817223 #Longitude, decimal degrees -180 to 180 
		city = 'Nairobi, KE'
		print('Using default location: {city}, Lat: {LA}, Lon: {LO}')
	else:
		city = args.city
		geolocator = geocoders.Nominatim(user_agent='Sun')  #geopy city->LA,LO locator
		location = geolocator.geocode(city)
		if location == None:
			print('Error with city input!, Kindly check.')
			exit()
		LA = location.latitude
		LO = location.longitude
		print('Using city input:', location)
		print(f'Lat: {LA}', 'Lon: {LO}')

	