import datetime
import numpy
from ms_boundaries_to_pdyn import ms_boundaries_to_pdyn
from pdyn_to_ms_boundaries import pdyn_to_mp, pdyn_to_bs
from tqdm import trange
import csv

from doy_to_ymd import *

import pandas




@numpy.vectorize
def amdadate_to_datetime(date):
    return datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%f")

def juno_ephemeris_from_amda(file):
    data_file = numpy.loadtxt(file,dtype="str")
    date = amdadate_to_datetime(data_file[:,0][:])
    x_coord = data_file[:,1].astype(float)
    y_coord = data_file[:,2].astype(float)
    z_coord = data_file[:,3].astype(float)

    return (date,x_coord,y_coord,z_coord)

def determine_juno_ephemeris_coordinates(time_start, time_end,date_ephem, x_coord,y_coord,z_coord, r_coord, th_coord, phi_coord):
	
	date_ephem_float = datetime_to_float(date_ephem)

	
	date_time = date_ephem[(date_ephem >= time_start) & (date_ephem <= time_end)]
	r_time = r_coord[(date_ephem >= time_start) & (date_ephem <= time_end)]
	th_time = th_coord[(date_ephem >= time_start) & (date_ephem <= time_end)]
	phi_time = phi_coord[(date_ephem >= time_start) & (date_ephem <= time_end)]
	x_time = x_coord[(date_ephem >= time_start) & (date_ephem <= time_end)]
	y_time = y_coord[(date_ephem >= time_start) & (date_ephem <= time_end)]
	z_time = z_coord[(date_ephem >= time_start) & (date_ephem <= time_end)]

	return(date_time, x_time, y_time, z_time, r_time, th_time, phi_time)


def boundary_crossings_caracteristics(time_datetime, directory_path="./", filename="boundary_crossings_caracteristics.csv", magnetopause=True, bow_shock=False):
	x_jso = []
	y_jso = []
	z_jso = []
	x_iau = []
	y_iau = []
	z_iau = []
	r = []
	th = []
	phi = []
	pdyn = []
	standoff_MP = []
	standoff_BS = []

	print("### Loading JSO ephemeris ###")
	# Loading JSO data to work with Joy et al (2002) model
	# to determine the Dynamic Pressure of the Solar Wind and the standoff distances
	(date_ephem_jso,x_coord_jso,y_coord_jso,z_coord_jso) = juno_ephemeris_from_amda("/Users/clouis/Documents/Data/JUNO/MAG_FGM/from_AMDA/ephemeris/juno_jup_xyz_jso_2016_2025.txt")
	r_coord_jso = numpy.sqrt(x_coord_jso**2 + y_coord_jso**2 + z_coord_jso**2)
	th_coord_jso = numpy.arccos(z_coord_jso / r_coord_jso)
	phi_coord_jso = numpy.arctan2(y_coord_jso,z_coord_jso)
	print("### JSO ephemeris Loaded ###")

	print("### Loading IAU ephemeris ###")
	(date_ephem_iau,x_coord_iau,y_coord_iau,z_coord_iau) = juno_ephemeris_from_amda("/Users/clouis/Documents/Data/JUNO/MAG_FGM/from_AMDA/ephemeris/juno_jup_xyz_iau_2016_2025.txt")
	r_coord_iau = numpy.sqrt(x_coord_iau**2 + y_coord_iau**2 + z_coord_iau**2)
	th_coord_iau = numpy.arccos(z_coord_iau / r_coord_iau)
	phi_coord_iau = numpy.arctan2(y_coord_iau,x_coord_iau)
	print("### IAU ephemeris Loaded ###")

	for i_ind in trange(len(time_datetime)):
		idatetime = time_datetime[i_ind]

		(date_tmp_jso,x_tmp_jso,y_tmp_jso,z_tmp_jso,r_tmp_jso,th_tmp_jso,phi_tmp_jso)=determine_juno_ephemeris_coordinates(idatetime-datetime.timedelta(seconds=150), idatetime+datetime.timedelta(seconds=150), date_ephem_jso,x_coord_jso,y_coord_jso, z_coord_jso, r_coord_jso, th_coord_jso, phi_coord_jso)
		x_jso.append(x_tmp_jso)
		y_jso.append(y_tmp_jso)
		z_jso.append(z_tmp_jso)
		
		pdyn_tmp = ms_boundaries_to_pdyn(x_tmp_jso[0],y_tmp_jso[0],z_tmp_jso[0],magnetopause = magnetopause, bow_shock = bow_shock)
		pdyn.append(pdyn_tmp)
		
		if pdyn_tmp[0] <= 2:
			([xdataptsed, xdataptsed],[yplotplused,yplotminused],standoff_tmp_MP) = pdyn_to_mp(Pdyn=pdyn_tmp, equatorial = True)
			([xdataptsed, xdataptsed],[yplotplused,yplotminused],standoff_tmp_BS) = pdyn_to_bs(Pdyn=pdyn_tmp, equatorial = True)

			if standoff_tmp_MP < standoff_tmp_BS:
				standoff_MP.append(standoff_tmp_MP)
				standoff_BS.append(standoff_tmp_BS)
			else: 
				standoff_MP.append(numpy.nan)	
				standoff_BS.append(numpy.nan)

		else:
			standoff_MP.append(numpy.nan)	
			standoff_BS.append(numpy.nan)

		(date_tmp,x_tmp_iau,y_tmp_iau,z_tmp_iau,r_tmp_iau,th_tmp_iau,phi_tmp_iau)=determine_juno_ephemeris_coordinates(idatetime-datetime.timedelta(seconds=150), idatetime+datetime.timedelta(seconds=150), date_ephem_iau,x_coord_iau,y_coord_iau, z_coord_iau, r_coord_iau, th_coord_iau, phi_coord_iau)
		x_iau.append(x_tmp_iau)
		y_iau.append(y_tmp_iau)
		z_iau.append(z_tmp_iau)
		r.append(r_tmp_iau)
		th.append(th_tmp_iau)
		phi.append(phi_tmp_iau)

	if magnetopause == True:
		boundary="magnetopause"
		bound="MP"
	if bow_shock == True:
		boundary="bow shock"
		bound="BS"
	with open(directory_path+filename, 'w') as file:
		writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		header = ['#',	"Day of Year",	"Date (year/month/day)",	"Time (HH:MM)",	"Boundary",	"In/Out",	"Notes",	"x (JSO)",	"y (JSO)",	"z (JSO)", "x (IAU)",	"y(IAU)",	"z (IAU)",	"r (IAU)",	"theta (IAU)",	"phi (IAU)",	"Dynamic Pressure (nPa)",	"Magnetopause Standoff Distance (Jovian radius)",	"Bow Shock Standoff Distance (Jovian radius)"]
		writer.writerow(header)
		

		for ielements in range(len(x_iau)):
			writer.writerow([
							bound+str(ielements+1),
							time_datetime[ielements].strftime("%j"),
							time_datetime[ielements].strftime("%Y/%m/%d"),
							time_datetime[ielements].strftime("%H:%M"),
							boundary,
							"",
							"",
							str("%3.3f" % x_jso[ielements][0]),
							str("%3.3f" % y_jso[ielements][0]),
							str("%3.3f" % z_jso[ielements][0]),
							str("%3.3f" % x_iau[ielements][0]),
							str("%3.3f" % y_iau[ielements][0]),
							str("%3.3f" % z_iau[ielements][0]),
							str("%3.3f" % r[ielements][0]),
							str("%3.3f" % th[ielements][0]),
							str("%3.3f" % phi[ielements][0]),
							str("%3.3f" % pdyn[ielements][0]),
							str("%3.3f" % standoff_MP[ielements]),
							str("%3.3f" % standoff_BS[ielements])
							])

	return(time_datetime,x_jso, y_jso,z_jso, x_iau, y_iau, z_iau,r,th,phi,pdyn,standoff_MP, standoff_BS)