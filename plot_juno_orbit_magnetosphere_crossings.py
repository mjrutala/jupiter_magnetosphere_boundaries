import datetime
import numpy

from retrieve_boundary_crossings_from_datetime.read_boundary_crossings_list import *
from read_juno_ephemeris_from_webgeocalc import *
from retrieve_boundary_crossings_from_datetime.pdyn_to_ms_boundaries import *
from read_juno_ephemeris_from_amda import *

def plot_juno_orbit_magnetosphere_crossings_2D(magnetopause_crossings = False, bow_shock_crossings = False,
											directory_path_out = "./",
					       						ephemeris_directory_path="./",
											add_juno_position = None,
											equatorial_plane = True, noon_midnight_plane = False, dawn_dusk_plane = False):
	# add_juno_position [optional]: datetime.datetime object
	

	if magnetopause_crossings == True:
		filename = "/Users/clouis/Documents/Etudes/Juno_jupiter_solar-wind_interaction/boundary_crossings_caracteristics_MP.csv"
	if bow_shock_crossings == True:
		filename = "/Users/clouis/Documents/Etudes/Juno_jupiter_solar-wind_interaction/boundary_crossings_caracteristics_BS.csv"

	
	(header, indice, date_cross, boundary, direction_crossing, notes, xyz_jss, xyz_iau, rtp_iau, pdyn, standoff_dist_mp, standoff_dist_bs) = read_boundary_crossings_list(filename)



	file_ephem = ephemeris_directory_path+"juno_jup_xyz_jss_2016_2022.txt"
	(date_ephem,x_coord,y_coord,z_coord) = juno_ephemeris_from_webgeocalc(file_ephem, planetary_radius = 71492.)
	
	if magnetopause_crossings:
		color = 'g'
		marker = 'o'
		color_marker = 'go'
		filename_out = directory_path_out+"full_MP_crossings_2D"
		date_beg = datetime.datetime(2016,6,20)
		date_end = datetime.datetime(2022,12,31)

	if bow_shock_crossings:
		color = 'b'
		marker = '^'
		color_marker = 'b^'
		filename_out = directory_path_out+"full_BS_crossings_2D"
		date_beg = datetime.datetime(2016,6,20)
		#date_end = datetime.datetime(2018,9,7,1,1)
		date_end = datetime.datetime(2022,12,31)

		
	x_plot = x_coord[(date_ephem >= date_beg) & (date_ephem <= date_end)]
	y_plot = y_coord[(date_ephem >= date_beg) & (date_ephem <= date_end)]
	z_plot = z_coord[(date_ephem >= date_beg) & (date_ephem <= date_end)]
	
	if equatorial_plane == True:
		plt.plot(y_plot, x_plot, 'k',)
	if noon_midnight_plane == True:
		plt.plot(x_plot, z_plot, 'k',)
	if dawn_dusk_plane == True:
		plt.plot(y_plot, z_plot, 'k')

	

	for i_crossing in range(len(date_cross)):
		x_cross = x_coord[(date_ephem >= date_cross[i_crossing]-datetime.timedelta(minutes = 2.5)) & (date_ephem <= date_cross[i_crossing]+datetime.timedelta(minutes = 2.5))]
		y_cross = y_coord[(date_ephem >= date_cross[i_crossing]-datetime.timedelta(minutes = 2.5)) & (date_ephem <= date_cross[i_crossing]+datetime.timedelta(minutes = 2.5))]
		z_cross = z_coord[(date_ephem >= date_cross[i_crossing]-datetime.timedelta(minutes = 2.5)) & (date_ephem <= date_cross[i_crossing]+datetime.timedelta(minutes = 2.5))]
		
		if equatorial_plane == True:
			plt.plot(y_cross, x_cross, color_marker)	
		if noon_midnight_plane == True:
			plt.plot(x_cross, z_cross, color_marker)	
		if dawn_dusk_plane == True:
			plt.plot(y_cross, z_cross, color_marker)
		
	
	if add_juno_position != None:
		for i_juno_position in add_juno_position:
			x_juno = x_coord[(date_ephem >= i_juno_position-datetime.timedelta(minutes = 2.5)) & (date_ephem <= i_juno_position+datetime.timedelta(minutes = 2.5))]
			y_juno = y_coord[(date_ephem >= i_juno_position-datetime.timedelta(minutes = 2.5)) & (date_ephem <= i_juno_position+datetime.timedelta(minutes = 2.5))]
			z_juno = z_coord[(date_ephem >= i_juno_position-datetime.timedelta(minutes = 2.5)) & (date_ephem <= i_juno_position+datetime.timedelta(minutes = 2.5))]
			
			color_marker_juno = 'r'+marker
			if equatorial_plane == True:
				plt.plot(y_juno, x_juno, color_marker_juno)
			if noon_midnight_plane == True:
				plt.plot(x_juno, z_juno, color_marker_juno)
			if dawn_dusk_plane == True:
				plt.plot(y_juno, z_juno, color_marker_juno)
	
	#adding Joy et al. (2002)'s model 10th and 90th percentile
	if magnetopause_crossings:
		if equatorial_plane == True:
			(x_eq_10,y_eq_10, standoff) = pdyn_to_mp(Pdyn=0.030, equatorial = True) #10th percentile
			(x_eq_50,y_eq_50, standoff) = pdyn_to_mp(Pdyn=0.209, equatorial = True) #10th percentile
			(x_eq_90,y_eq_90, standoff) = pdyn_to_mp(Pdyn=0.518, equatorial = True) #10th percentile
		if noon_midnight_plane == True:
			(x_eq_10,y_eq_10, standoff) = pdyn_to_mp(Pdyn=0.030, noon_midnight = True) #10th percentile
			(x_eq_50,y_eq_50, standoff) = pdyn_to_mp(Pdyn=0.209, noon_midnight = True) #50th percentile
			(x_eq_90,y_eq_90, standoff) = pdyn_to_mp(0.518, noon_midnight = True) #90th percentile
		if dawn_dusk_plane == True:
			(x_eq_10,y_eq_10, standoff) = pdyn_to_mp(Pdyn=0.030, dawn_dusk = True) #10th percentile
			(x_eq_50,y_eq_50, standoff) = pdyn_to_mp(Pdyn=0.209, dawn_dusk = True) #50th percentile
			(x_eq_90,y_eq_90, standoff) = pdyn_to_mp(Pdyn=0.518, dawn_dusk = True) #90th percentile
		
	if bow_shock_crossings:
		if equatorial_plane == True:
			(x_eq_10,y_eq_10, standoff) = pdyn_to_bs(Pdyn=0.063, equatorial = True) #10th percentile
			(x_eq_50,y_eq_50, standoff) = pdyn_to_bs(Pdyn=0.258, equatorial = True) #50th percentile
			(x_eq_90,y_eq_90, standoff) = pdyn_to_bs(Pdyn=0.579, equatorial = True) #90th percentile
		if noon_midnight_plane == True:
			(x_eq_10,y_eq_10, standoff) = pdyn_to_bs(Pdyn=0.063, noon_midnight = True) #10th percentile
			(x_eq_50,y_eq_50, standoff) = pdyn_to_bs(Pdyn=0.258, noon_midnight = True) #50th percentile
			(x_eq_90,y_eq_90, standoff) = pdyn_to_bs(Pdyn=0.579, noon_midnight = True) #90th percentile
		if dawn_dusk_plane == True:
			(x_eq_10,y_eq_10, standoff) = pdyn_to_bs(Pdyn=0.063, dawn_dusk = True) #10th percentile
			(x_eq_50,y_eq_50, standoff) = pdyn_to_bs(Pdyn=0.258, dawn_dusk = True) #50th percentile
			(x_eq_90,y_eq_90, standoff) = pdyn_to_bs(Pdyn=0.579, dawn_dusk = True) #90th percentile


	if equatorial_plane == True:
		plt.plot(y_eq_10[0], x_eq_10[0], '--', color = "k")
		plt.plot(y_eq_10[1], x_eq_10[1], '--', color = "k")
		#plt.plot(y_eq_50[0], x_eq_50[0], '-', color = "r")
		#plt.plot(y_eq_50[1], x_eq_50[1], '-', color = "r")
		plt.plot(y_eq_90[0], x_eq_90[0], ':', color = "k")
		plt.plot(y_eq_90[1], x_eq_90[1], ':', color = "k")
	
		plt.xlim(-150, +150)
		plt.ylim(+60, -120)
		plt.xlabel("y (JSS)")
		plt.ylabel("x (JSS)")
		view = "_equatorial"
	
	if noon_midnight_plane == True:
		plt.plot(x_eq_10[0], y_eq_10[0], '-', color = "g")
		plt.plot(x_eq_10[1], y_eq_10[1], '-', color = "g")
		#plt.plot(x_eq_50[0], y_eq_50[0], '-', color = "r")
		#plt.plot(x_eq_50[1], y_eq_50[1], '-', color = "r")
		plt.plot(x_eq_90[0], y_eq_90[0], '-', color = "b")
		plt.plot(x_eq_90[1], y_eq_90[1], '-', color = "b")
		
		plt.xlim(-100, +20)
		plt.ylim(-40, +30)
		plt.xlabel("x (JSS)")
		plt.ylabel("z (JSS)")
		view = "_noon-midnight"

	if dawn_dusk_plane == True:
		plt.plot(x_eq_10[0], y_eq_10[0], '-', color = "g")
		plt.plot(x_eq_10[1], y_eq_10[1], '-', color = "g")
		#plt.plot(x_eq_50[0], y_eq_50[0], '-', color = "r")
		#plt.plot(x_eq_50[1], y_eq_50[1], '-', color = "r")
		plt.plot(x_eq_90[0], y_eq_90[0], '-', color = "b")
		plt.plot(x_eq_90[1], y_eq_90[1], '-', color = "b")
		
		plt.xlim(-100, +20)
		plt.ylim(-40, +30)
		plt.xlabel("y (JSS)")
		plt.ylabel("z (JSS)")
		view = "_dawn-dusk"

	plt.tight_layout()
	plt.savefig(filename_out+view+".pdf", dpi = 500)

	plt.close()

	return


def plot_juno_orbit_magnetosphere_crossings_3D(magnetopause_crossings = False, bow_shock_crossings = False,
											directory_path_out = "./",
					       						ephemeris_directory_path="./",
											add_juno_position = None, JSS = False, JH = False, JSO = False, IAU = False):
	# add_juno_position [optional]: datetime.datetime object
	

	if magnetopause_crossings == True:
		filename = "/Users/clouis/Documents/Etudes/Juno_jupiter_solar-wind_interaction/boundary_crossings_caracteristics_MP.csv"
	if bow_shock_crossings == True:
		filename = "/Users/clouis/Documents/Etudes/Juno_jupiter_solar-wind_interaction/boundary_crossings_caracteristics_BS.csv"
	(header, indice, date_cross, boundary, direction_crossing, notes, xyz_jss, xyz_iau, rtp_iau, pdyn, standoff_dist_mp, standoff_dist_bs) = read_boundary_crossings_list(filename)

	if JSS == False and JH == False and JSO == False and IAU == False:
		print("### Users must choose a coordinate system ###")
		return

	if JSS == True:
		file_ephem = ephemeris_directory_path+"juno_jup_xyz_jss_2016_2022.txt"
		(date_ephem,x_coord,y_coord,z_coord) = juno_ephemeris_from_webgeocalc(file_ephem, planetary_radius = 71492.)
		coord_name = "JSS"
	if JH == True:
		file_ephem = ephemeris_directory_path+"juno_jup_xyz_jh_2016_2022.txt"
		(date_ephem,x_coord,y_coord,z_coord) = juno_ephemeris_from_webgeocalc(file_ephem, planetary_radius = 71492.)
		coord_name = "JH"
	if JSO == True:
		file_ephem = ephemeris_directory_path+"juno_jup_xyz_jso_2016_2025.txt"
		(date_ephem,x_coord,y_coord,z_coord) = juno_ephemeris_from_amda(file_ephem)
		coord_name = "JSO"
	if IAU == True:
		file_ephem = ephemeris_directory_path+"juno_jup_xyz_iau_2016_2025.txt"
		(date_ephem,x_coord,y_coord,z_coord) = juno_ephemeris_from_amda(file_ephem)
		coord_name = "IAU"

	fig = plt.figure(figsize = (10,10))
	ax = plt.axes(projection="3d")
	
	# draw sphere
	u, v = numpy.mgrid[0:2*numpy.pi:50j, 0:numpy.pi:50j]
	r = 1.
	c = [0.,0.,0.]
	x = r*numpy.cos(u)*numpy.sin(v)
	y = r*numpy.sin(u)*numpy.sin(v)
	z = r*numpy.cos(v)
	
	ax.plot_surface(x-c[0], y-c[1], z-c[2], color=('k'))
	
	plt.title("Juno's orbit ("+coord_name+" coordinates)")
	ax.set_xlabel("x ("+coord_name+")")
	ax.set_ylabel("y ("+coord_name+")")
	ax.set_zlabel("z ("+coord_name+")")
	

	
	if magnetopause_crossings:
		color = 'g'
		marker = 'o'
		color_marker = 'go'
		filename_out = directory_path_out+"full_MP_crossings_3D"
		date_beg = datetime.datetime(2016,6,20)
		date_end = datetime.datetime(2022,12,31)

	if bow_shock_crossings:
		color = 'b'
		marker = '^'
		color_marker = 'b^'
		filename_out = directory_path_out+"full_BS_crossings_3D"
		date_beg = datetime.datetime(2016,6,20)
		#date_end = datetime.datetime(2018,9,7,1,1)
		date_end = datetime.datetime(2022,12,31)

	filename_out = filename_out+"_"+coord_name

	x_plot = x_coord[(date_ephem >= date_beg) & (date_ephem <= date_end)]
	y_plot = y_coord[(date_ephem >= date_beg) & (date_ephem <= date_end)]
	z_plot = z_coord[(date_ephem >= date_beg) & (date_ephem <= date_end)]
		
	ax.plot3D(x_plot, y_plot, z_plot, color = 'k')


	for i_crossing in range(len(date_cross)):
		x_cross = x_coord[(date_ephem >= date_cross[i_crossing]-datetime.timedelta(minutes = 2.5)) & (date_ephem <= date_cross[i_crossing]+datetime.timedelta(minutes = 2.5))]
		y_cross = y_coord[(date_ephem >= date_cross[i_crossing]-datetime.timedelta(minutes = 2.5)) & (date_ephem <= date_cross[i_crossing]+datetime.timedelta(minutes = 2.5))]
		z_cross = z_coord[(date_ephem >= date_cross[i_crossing]-datetime.timedelta(minutes = 2.5)) & (date_ephem <= date_cross[i_crossing]+datetime.timedelta(minutes = 2.5))]
		ax.plot3D(x_cross, y_cross, z_cross, c = color,marker = marker)	
	

	if add_juno_position != None:
		for i_juno_position in add_juno_position:
			x_juno = x_coord[(date_ephem >= i_juno_position-datetime.timedelta(minutes = 2.5)) & (date_ephem <= i_juno_position+datetime.timedelta(minutes = 2.5))]
			y_juno = y_coord[(date_ephem >= i_juno_position-datetime.timedelta(minutes = 2.5)) & (date_ephem <= i_juno_position+datetime.timedelta(minutes = 2.5))]
			z_juno = z_coord[(date_ephem >= i_juno_position-datetime.timedelta(minutes = 2.5)) & (date_ephem <= i_juno_position+datetime.timedelta(minutes = 2.5))]
			
		
			color = 'r'
			color_marker_juno = color+marker
			ax.plot3D(x_juno, y_juno, z_juno, c = 'r', marker = marker)	



	plt.tight_layout()
	
	for i_azim in range(0,360,30):
		ax.view_init(elev = 10,azim=i_azim)
		plt.savefig(filename_out+"%d.pdf" %i_azim, dpi = 500)
	
	plt.close()
	
	
	return
