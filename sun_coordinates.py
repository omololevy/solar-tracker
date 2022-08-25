from . import get_inputs
import pytz
import datetime as dt
import numpy as np
from numpy import sin,cos,arctan,arccos

def sun_coords(date_time_local, LA, LO):
	'''
	Purpose: Calculate sun angles from time and position on earth
	Inputs 
		date_time_local: date_time_object with timezone attached
		LA: decimal latitude
		LO: decimal longitude
	Outputs
		Theta: [radians] Angle measured clockwise from due east to the point on the horizon underneath the sun
		Phi: [radians] Angle from the vertical pointing to the sun from the perspective of a person standing on the surface
		Theta_from_North: [deg] Clockwise angle from due north to the point on the horizon underneath the sun
		Phi_from_Horizon: [deg] Vertical angle from horizon to sun  
	'''
	
	