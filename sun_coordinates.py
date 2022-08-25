import pytz
import datetime as dt
import numpy as np
from numpy import sin,cos,arctan,arccos


def sun_coordinates(date_time_local, LA, LO):
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
	
	date_time_utc = date_time_local.astimezone(pytz.utc) #get date_time_local time in utc timezone
	t_input = date_time_utc.replace(tzinfo=None) #eliminate timezone attribute to make time subtraction simpler

	# define constants we'll need for orbital calculations

	PI = np.pi
	rEO = 149600000 #radius earth orbit, km
	rE = (6378 + 6357)/2 #radius earth, km
	phiE = 23.4*PI/180 #earth tilt, degrees
	tday = 86164.0905 # seconds in a sidereal day (time needed for earth to rotate 360 degrees, but everyday it actually rotates a little bit more because of the earth's orbit around the sun
	tyear = 366.25*tday #seconds in a year, note: there are 366.25 sidereal days in a year
	t0 = dt.datetime(2020, 3, 20, 12, 0, 0) #initial condition - when sun was directly overhead of latitude 0, longitude 0 on the spring equinox of 2020
	tdiff = t_input - t0 #the difference in time between this initial condition and the time we're calculating forms the basis of our calculations 
	t = tdiff.total_seconds() 


	####Thetas and Phis######

	TLL = PI/180*LO + 2*PI/tday*t + PI #Theta of the latitude longitude coordinates in the earth's reference frame
	PLL = PI/2 - 2*PI/360*LA #Phi of the Latitude Longitude in the earth's reference frame
	TEO = 2*PI/tyear*t #Theta of earth orbit in the sun's reference frame, 0 radians is spring equinox

	# Three componenets of a vector pointing to the sun in the reference frame of a person standing on the earth's surface
	Perp = rEO*(sin(phiE)*sin(TEO)*cos(PLL) - cos(phiE)*sin(TEO)*sin(TLL)*sin(PLL) - cos(TEO)*cos(TLL)*sin(PLL)) - rE    
	North = rEO*(sin(phiE)*sin(TEO)*sin(PLL) + cos(phiE)*sin(TEO)*sin(TLL)*cos(PLL) + cos(TEO)*cos(TLL)*cos(PLL))
	East = rEO*(cos(TEO)*sin(TLL) - cos(phiE)*sin(TEO)*cos(TLL))

	
	Theta_raw = arctan(North/East)   #Angle measured clockwise from due east to the point on the horizon underneath the sun, 0 radians is due east
	Theta_deg = Theta_raw*180/PI
	
	#Correcting Theta depending on the unit circle "quadrant" the sun is in, and calculating circular angle from due north
	if North > 0 and East > 0:
		Theta_from_North = 90 - Theta_deg
	
	if North > 0 and East < 0:
		Theta_deg = Theta_deg + 180
		Theta_from_North = 450 - Theta_deg
	
	if North < 0 and East < 0:
		Theta_deg = Theta_deg + 180
		Theta_from_North = 450 - Theta_deg

	if North < 0 and East > 0:
		Theta_deg = Theta_deg + 360
		Theta_from_North = 450 - Theta_deg

	Theta = Theta_deg*PI/180
	Theta_from_North = int(Theta_from_North)

	Phi = arccos(Perp/np.sqrt(Perp*Perp + North*North + East*East))  #Angle from the vertical that points to the sun in the reference frame of a person standing on the earth's surface
	Phi_from_Horizon = int(90 - Phi*360/(2*PI))

	return Theta, Phi, Theta_from_North, Phi_from_Horizon