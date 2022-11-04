#−∗− coding : utf−8 −∗−

import numpy as np
import datetime
import numpy

@np.vectorize
def doy_to_ymd(doy,hours,minutes,second):
    ### Function to change a (doy (in yyyyddd format), hours, minutes, second) to a datetime object datetime.datetime(YYYY, mm, dd, HH, MM, SS)
    return datetime.datetime.strptime(doy+hours+minutes+second,'%Y%j%H%M%S.%f')


def doy_to_datetime(time_doy):
    ### Function to change a doy (in floating yyyyddd format) to a datetime object datetime.datetime(YYYY, mm, dd, HH, MM, SS)
    time_hours = [int((itime-int(itime))*24) for itime in (time_doy)]
    time_minutes = [int(((time_doy[itime]-int(time_doy[itime]))*24-time_hours[itime])*60) for itime in range(len(time_doy))]
    time_seconds = [int((((time_doy[itime]-int(time_doy[itime]))*24-time_hours[itime])*60-time_minutes[itime])*60) for itime in range(len(time_doy))]
    time = [datetime.datetime.strptime(f'{int(time_doy[itime])}T{time_hours[itime]:02d}:{time_minutes[itime]:02d}:{time_seconds[itime]:02d}', "%Y%jT%H:%M:%S") for itime in range(len(time_doy))]
    return(time)


@np.vectorize
def doy_float_to_ymd(doy,hours):
    ### Function to transform a doy YYYYDDD in floating format to a datetime object
    ymd = datetime.datetime.strptime((doy)[0:7],'%Y%j')
    daydec = datetime.timedelta(hours=(hours))
    return (ymd + daydec)

@np.vectorize
def return_hour_minute(date):
    ### Function to return only the hour and minute of a datetime object
    result = datetime.datetime.strftime(date,'%H:%M')
    return (result)

@numpy.vectorize
def datetime_to_float(datetime_table):
    ### Function to return time in floating format (from a datetime object)
    return datetime_table.timestamp()

def doy_specific_year_to_yyyyddd(doy, origin):  
### Function to change "day of a specific year" format to yyyyddd ###

    aa = np.arange(61, dtype=float)+origin  # array of years starting from year of origin
    deb = np.zeros([61], dtype=float)  # zeros
    for i in range(1, len(deb)):  # categorising start point for each year
        if i % 4 == 1:
            deb[i:] = deb[i:]+366.
        else:
            deb[i:] = deb[i:]+365.

    yyyyddd = np.zeros(len(doy), dtype=float)

    for i in range(0, len(doy)):
        j = doy[i]-deb
        yyyyddd[i] = (aa[j >= 1][-1])*1000.+j[j >= 1][-1]

    return(yyyyddd)
