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
