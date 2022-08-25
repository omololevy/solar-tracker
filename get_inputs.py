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
		print(f'Using default location: {city}, Lat: {LA}, Lon: {LO}')
	else:
		city = args.city
		geolocator = geocoders.Nominatim(user_agent='Sun')  #geopy city->LA,LO locator
		location = geolocator.geocode(city)
		if location == None:
			print('Error with city input!, Kindly check.')
			exit()
		LA = location.latitude
		LO = location.longitude
		print(f'Using city input {location}')
		print(f'Lat: {LA}', 'Lon: {LO}')

	# get timezone from LA and LO
	tz = tzwhere.tzwhere(forceTZ=True)  #initialize timezone finder 
	timezone = pytz.timezone(tz.tzNameAt(LA, LO, forceTZ=True))

	#date and time input
	if args.date_time == None:  #if no time provided, get the current in the timezone of interest
		date_time_local = dt.datetime.now(timezone)    
		print(f'Using default time (current time at location) {date_time_local}')
	else:
		try: 
			date_time = dt.datetime.strptime(args.date_time, '%Y-%m-%d %H:%M:%S')
			date_time_local = timezone.localize(date_time)
			print(f'Using time input {date_time_local}')
		except:
			print('Error with time input, ensure format is %Y-%m-%d %H:%M:%S')
			exit()

	
	print(f'Using timezone {timezone}')
	   #attach timezone to date_time making it aware

	return date_time_local, LA, LO, city