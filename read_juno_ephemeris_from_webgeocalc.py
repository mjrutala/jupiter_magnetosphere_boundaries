import numpy
import datetime

@numpy.vectorize
def webgeocalc_date_to_datetime(date_YMD,date_hours):
        return datetime.datetime.strptime(date_YMD+"T"+date_hours,"%Y-%m-%dT%H:%M:%S.%f")

def juno_ephemeris_from_webgeocalc(file, planetary_radius=False):
    if planetary_radius == False:
        print("### User needs to give a planetary radius to have ephemeris in planetary units ###")
    data_file = numpy.loadtxt(file,dtype="str")
    date = webgeocalc_date_to_datetime(data_file[:,0],data_file[:,1])
    x_coord = data_file[:,5].astype(float)
    y_coord = data_file[:,6].astype(float)
    z_coord = data_file[:,7].astype(float)

    return (date,x_coord[:]/planetary_radius,y_coord[:]/planetary_radius,z_coord[:]/planetary_radius)
