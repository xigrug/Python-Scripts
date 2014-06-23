########################################
# Read station radiosonde files in and get info on sounding times, dates, and heights reached
#
# Created by: Peter Willetts
# Created on: 14/5/2014
#
########################################
#
# http://www1.ncdc.noaa.gov/pub/data/igra/readme.txt
###################################################

import glob
import re
import numpy as np

# Create list of monthly radiosonde files to be used as input
# Derived parameters .dat files
#rad_flist = glob.glob ('/nfs/a90/eepdw/Data/Observations/Radiosonde_downloaded_from_NOAA_GUAN/*.dat')
rad_flist = glob.glob ('/nfs/a90/eepdw/Data/Observations/Radiosonde_downloaded_from_NOAA_GUAN/*.dat')
match_header = re.compile(r'#*20110[89]')

station_list='/nfs/a90/eepdw/Data/Observations/Radiosonde_downloaded_from_NOAA_GUAN/igra-stations.txt'

# Read station name files searching for start of each indpendent sounding header

station_metadata=[]
f = open(station_list,'r')
for line in f:
     line = line.strip()
     line=re.sub(r'([A-Z])\s([A-Z])', r'\1_\2',line)
     line=re.sub(r'([A-Z])\s\s([A-Z])', r'\1_\2',line)
     station_metadata.append(line.split())

f.close()

# Read station files searching for start of each indpendent sounding header
all_stations_soundings=[]

for i in rad_flist:
    sounding=[]
    station_soundings=[]
    station_no=i[-9:-4]
    match_filename = re.compile('%s' % station_no)
    for sm in station_metadata:
        if match_filename.search(str(sm)) is not None:
            station=sm[2]
            latitude=sm[3]
            longitude=sm[4]
            #GUAN_code=sm[6]
            
            #print station
    #print i
    f = open(i,'r')

    for line in f:
     line = line.strip()
     columns = line.split()
     #print line
# Extract independent header variable
    
     if match_header.search(line) is not None:
      #print line
      date=columns[0][1:14]
      time=columns[0][16:20]
      time_hour=columns[0][14:16]
      #print time_hour
      #print columns[0][1:17]
      no_levels=columns[1]
      sounding=(date, time, time_hour, no_levels)
      station_soundings.append(sounding)
    all_stations_soundings.append((station, latitude, longitude, station_soundings))

np.save('/nfs/a90/eepdw/Data/Observations/Radiosonde_downloaded_from_NOAA_GUAN/Embrace_Period_India_Station_and_sounding_Info_measured', np.array(all_stations_soundings, dtype=object))
#np.save('/nfs/a90/eepdw/Data/Observations/Radiosonde_downloaded_from_NOAA_GUAN/Embrace_Period_India_Station_and_sounding_Info_derived', np.array(all_stations_soundings, dtype=object))