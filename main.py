import argparse
import get_inputs
import sun_coordinates
import make_3D_plot

def main(args):
    	
	# get time, lat, and long from input args or default values
	date_time_local, LA, LO, city = get_inputs.get_inputs(args)

	# get Theta, Phi angles for sun (see documentation for definitions)
	Theta, Phi, Theta_from_North, Phi_from_Horizon = sun_coordinates.sun_coordinates(date_time_local, LA, LO)

	print('Theta from North =', Theta_from_North)
	print('Phi from Horizon =', Phi_from_Horizon)

	make_3D_plot(Theta, Phi, Theta_from_North, Phi_from_Horizon, date_time_local, LA, LO, city, args.save_plot)



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--date_time', default=None)
	parser.add_argument('-c', '--city', default=None)
	parser.add_argument('-p', '--save_plot', default=False)
	args = parser.parse_args()
	main(args)