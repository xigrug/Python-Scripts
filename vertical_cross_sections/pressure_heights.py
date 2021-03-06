"""

Load geopotential heights and orography cube to get lat/lon cross-section

22/05/14

"""

import os, sys


import iris
import iris.analysis.cartography

import h5py

import numpy as np

c_section_lon=74.
c_section_lat=0

diags=['408','temp', 'sp_hum']
experiment_ids = ['djznw', 'djzny', 'djznq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'djzns', 'dkjxq'  ]
#experiment_ids = ['dklyu', 'dkmbq', 'dklwu', 'dklzq' ]
#experiment_ids = ['dkbhu']
#experiment_ids = ['djzny']

for experiment_id in experiment_ids:
  expmin1 = experiment_id[:-1]
  f_oro =  '/nfs/a90/eepdw/Data/EMBRACE/Mean_State/pp_files/%s/%s/33.pp' % (expmin1, experiment_id)
  oro = iris.load_cube(f_oro)

  cs = oro.coord_system('CoordSystem')
  csur=cs.ellipsoid  

  lat = oro.coord('grid_latitude').points
  lon = oro.coord('grid_longitude').points

  lons, lats = np.meshgrid(lon, lat)  
  lons,lats = iris.analysis.cartography.unrotate_pole(lons,lats, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)

  lon=lons[0]
  lat=lats[:,0]

  
        

  for i, coord in enumerate (oro.coords()):
     if coord.standard_name=='grid_latitude':
         lat_dim_coord_oro = i
     if coord.standard_name=='grid_longitude':
         lon_dim_coord_oro = i

  oro.remove_coord('grid_latitude')
  oro.remove_coord('grid_longitude')
  oro.add_dim_coord(iris.coords.DimCoord(points=lat, standard_name='grid_latitude', units='degrees', coord_system=csur), lat_dim_coord_oro)
  oro.add_dim_coord(iris.coords.DimCoord(points=lon, standard_name='grid_longitude', units='degrees', coord_system=csur), lon_dim_coord_oro)
  print oro


  l=oro.coord('grid_longitude').nearest_neighbour_index(c_section_lon)

  for diag in diags:
   
   try:
       file_h='/nfs/a90/eepdw/Data/EMBRACE/Pressure_level_means/%s_pressure_levels_interp_%s_mean_masked' % (diag,experiment_id)
       with h5py.File(file_h, 'r') as f:
           data=f['mean'][. . .]
   except IOError:
       file_h='/nfs/a90/eepdw/Data/EMBRACE/Pressure_level_means/%s_pressure_levels_interp_pressure_%s_mean_masked' % (diag,experiment_id)
       with h5py.File(file_h, 'r') as f:
           data=f['mean'][. . .]

   print diag
   print file_h
   

   if (c_section_lon != 0):
     xc=data[:,l,:]
     np.savez('/nfs/a90/eepdw/Data/EMBRACE/Cross_Sections/%s_%s_height_XC_Longitude_%s' % (experiment_id, diag, c_section_lon), xc=xc, coord=oro.coord('grid_latitude').points)
   if (c_section_lat != 0):
     xc=data[l,:,:]
     np.savez('/nfs/a90/eepdw/Data/EMBRACE/Cross_Sections/%s_%s_height_XC_Latitude_%s' % (experiment_id, diag, c_section_lat), xc=xc, coord=oro.coord('grid_longitude').points)

   print xc
   print xc.shape
   print oro.coord('grid_latitude').points
   print oro.coord('grid_latitude').points.shape
     
