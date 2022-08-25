import sun_coordinates
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
from numpy import sin,cos,arctan,arccos
import datetime as dt


def make_3D_plot(Theta, Phi, Theta_from_North, Phi_from_Horizon, date_time_local, LA, LO, city, save_plot=False):
	'''
	Purpose: Generate 3D plot visualing where the sun is with respect to the cardinal directions from the perspecitve of a person standing on the surface of the earth
	Inputs
		Theta: [radians] Angle measured clockwise from due east to the point on the horizon underneath the sun
		Phi: [radians] Angle from the vertical pointing to the sun from the perspective of a person standing on the surface
		Theta_from_North: [deg] Clockwise angle from due north to the point on the horizon underneath the sun
		Phi_from_Horizon: [deg] Vertical angle from horizon to sun 
		date_time_local: date_time_object with timezone attached
		LA: decimal latitude
		LO: decimal longitude
	Outputs
		3D plot
	''' 
	#3D plot of sun location
	fig = plt.figure(figsize=(10, 8))
	ax = fig.add_subplot(111, projection='3d')
	ax.axis('off')

	# Create the mesh in polar coordinates and compute corresponding Z.
	radPL = 1
	thePL = np.linspace(0, 2*np.pi, 50)
	phiPL = np.linspace(0, 0.5*np.pi, 200)
	ThePL, PhiPL  = np.meshgrid(thePL, phiPL)

	#Plot a dome 
	XD = radPL*cos(ThePL)*sin(PhiPL)
	YD = radPL*sin(ThePL)*sin(PhiPL)
	ZD = radPL*cos(PhiPL)
	ax.plot_surface(XD, YD, ZD, alpha = 0.2)

	#Plot cardinal directions
	ax.plot3D(np.linspace(-1, 1, 50), np.linspace(0, 0, 50), np.linspace(0, 0, 50), color='black')
	ax.plot3D(np.linspace(0, 0, 50), np.linspace(0, 1, 50), np.linspace(0, 0, 50), color='red')
	ax.text(0, 1, 0, "N", color='red', size=14)
	ax.plot3D(np.linspace(0, 0, 50), np.linspace(-1, 0, 50), np.linspace(0, 0, 50), color='black')

	#Plot vector pointing to the current location of the sun
	R = np.linspace(0, 1, 50)
	X = cos(Theta)*sin(Phi)
	Y = sin(Theta)*sin(Phi)
	Z = cos(Phi)

	#Generating single value linspaces for the dashed guide lines
	Xspace = np.linspace(X, X, 50)
	Yspace = np.linspace(Y, Y, 50)
	
	if Phi < np.pi/2: #only plot if sun is above horizon
		ax.plot3D(R*X, R*Y, 0, color='black', dashes=[6, 2]) #dashed line in xy plane
		ax.plot3D(Xspace, Yspace, R*Z, color='black', dashes=[6, 2]) #vertical dashed line
		ax.plot3D(R*X, R*Y, R*Z, color='black') #line from origin to sun
		ax.scatter3D(X, Y, Z, s=1000, color='gold') # sun object itself
	
	
	#Text labels on graph
	time_label = dt.datetime.strftime(date_time_local, '%H:%M %m-%d-%Y')
	city_label = 'City: ' + city
	theta_phi_label = f'Theta: {Theta_from_North} deg\nPhi: {Phi_from_Horizon} deg'
	label = 'Time: ' + time_label + '\n' + city_label + '\n' + theta_phi_label
	ax.text(1.2, 0, 1.2, label,
         size=14,
         color='black',
         horizontalalignment='center',
         verticalalignment='top',
         multialignment='left')

	#Plot arc representing the path of the sun in the sky
	time = date_time_local

	hourspan = range(0,24)
	minutespan = range(0, 60, 20)
	Xspan = []
	Yspan = []
	Zspan = []
	for hour in hourspan:
		for minute in minutespan:
			time = time.replace(minute = minute, hour=hour)
			Theta, Phi, Theta_from_North, Phi_from_horizon = sun_coordinates.sun_coordinates(time, LA, LO)
			if Phi < np.pi/2: #only plot if sun is above horizon
				X = cos(Theta)*sin(Phi)
				Y = sin(Theta)*sin(Phi)
				Z = cos(Phi)
				Xspan.append(X)
				Yspan.append(Y)
				Zspan.append(Z)
				if minute == 0:
					ax.text(X, Y, Z, hour, color='black', horizontalalignment='center')
		
	ax.plot3D(Xspan, Yspan, Zspan, color='gold')

	
	# Set Plot Boundaries
	ax.set_xlim(-1, 1)
	ax.set_ylim(-1, 1)
	ax.set_zlim(0, 1)
	ax.set_xlabel('X/West-East')
	ax.set_ylabel('Y/North-South')
	ax.set_zlabel('Z')
	
	plt.subplots_adjust(left=0, bottom=0, right=1, top=0.8)
	plt.show()

	if save_plot:
		fig.savefig(save_plot)
