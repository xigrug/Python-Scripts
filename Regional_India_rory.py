########################################
# Regional_Lebel_TRMM.py
#
# Created by: Rory Fitzptrick
# Created on: 20.10.2013
#
########################################
#
# This program will take regional data
# across region 10W-10E and calculate
# the total number of rain events
# per day across the region with
# 10 day smoothing.
#
# In order to do this from 3hrly
# data the following shall be done:
#
# - Take TRMM data for 3hr space for entire day (3d data)
# - for each latitude, at each gridcell
# establish whether rain fell or not
# - If yes, give value of 1, if not give
#  value of 0
# - If yes, go through rest of day and establish
# length of rain period and if there was more than
# 1 rain event in the day.
# - If there is rain at end of day, hold value of 
# 1 in keeper array (2-d), else 0
# - For next day, if value in keeper array is 0,
# only start counting rain events after first rain 
# free period.
#
# Output will be 3-d array (lat, lon, days) with
# integer values
#
###################################################

def Regional_India(yy):
 import matplotlib.pyplot as plt
 import numpy as np
 from netCDF4 import Dataset
 import os

# constants
# lon from 10W - 10E
# lat from 0 - 15N

lon_amounts = 80
lat_amounts = 120
dys = 31+30
hrs = [0,3,6,9,12,15,18,21]
monthyet = [0,31]
# lats = np.linspace[0,15,80]
# tme = np.linspace[119,119+dys,dys]
# create master array
 diurn = np.zeros((8), dtype = float)
 mastr = np.zeros((lat_amounts, lon_amounts, dys),dtype =int) 

# Outer 2 loops are going to be month and date
 overnight_holdall = np.zeros((lat_amounts,lon_amounts), dtype = int)

 for mnth in range(8,10): 
    for dte in['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']:
        # will first test if first file exists
       fle = '3B42.0'+str(yy)+'0'+str(mnth)+str(dte)+'.0.6.nc'      
       if os.path.isfile(fle):
# if file exists run code
            # create holder array for day date
            print fle
            prec_dat = np.zeros((lat_amounts,lon_amounts,8),dtype = float)
            # create check_day
            check_day = int(dte) + int(monthyet[mnth-8])
            # now import files
            for h in hrs:
                nc = Dataset('3B42.0'+str(yy)+'0'+str(mnth)+str(dte)+'.'+str(h)+'.6.nc')
                trmm = nc.variables['precipitation']
                # data crosses zero line so will need to cut it
                mat = trmm[160:280, 1200:1280]
                nc.close()
                # transfer data into prec_dat
                prec_dat[:,:,h/3] = mat[:]
                for lat in range(0,lat_amounts):
                   for lon in range(0,lon_amounts):
                      if prec_dat[lat,lon,h/3] <= 0:
                        continue
                      else:
                         diurn[h/3] = diurn[h/3] + prec_dat[lat,lon,h/3] 
                print diurn[h/3]                             
       else:
            print  'error'
            continue
            

# average the rain value for each day, at each gridcell with t flexible
# will produce a plot of time against precip

 tme = []
 for t in range(0,8):
    tme.extend([t*3])
 diurn[:] = diurn[:]/(dys*lat_amounts*lon_amounts)
 plt.plot(tme,diurn)
 plt.xlabel('Time')
 plt.ylabel('Precipitation (mm)')
 plt.title('Diurnal cycle 2006')
 plt.show()

 
            
if '__name__' == '__Regional_India__':
  Regional_India(yy)                                    
