"""

Load pp, plot and save


"""

import os, sys

import matplotlib

matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
from matplotlib import rc
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams

rc('font', family = 'serif', serif = 'cmr10')
rc('text', usetex=True)

rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True

rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True
rcParams['font.family']='serif'
rcParams['font.serif']='cmr10'

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as mpl_cm
import numpy as np

import iris
import iris.coords as coords
import iris.quickplot as qplt
import iris.plot as iplt
import iris.coord_categorisation

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import datetime
from mpl_toolkits.basemap import cm

import imp
from textwrap import wrap

import re

import iris.analysis.cartography

import math

save_path='/nfs/a90/eepdw/Figures/EMBRACE/'

model_name_convert_title = imp.load_source('util', '/nfs/see-fs-01_users/eepdw/python_scripts/modules/model_name_convert_title.py')
unrotate = imp.load_source('util', '/nfs/see-fs-01_users/eepdw/python_scripts/modules/unrotate_pole.py')

pp_file = 'rain_mean'

pp_file_dir ='/nfs/a90/eepdw/Data/EMBRACE/Mean_State/pp_files/'

degs_crop_top = 1.7
degs_crop_bottom = 2.5

min_contour = 0
max_contour = 3.5
tick_interval=0.5
#
# cmap= cm.s3pcpn_l

divisor=10  # for lat/lon rounding

def main():

 #experiment_ids = ['djzns', 'djznq', 'djzny', 'djznw', 'dkhgu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq','dkbhu' ] 
 
 experiment_ids = ['dkbhu', 'djznu', 'dkhgu' ] 
 #experiment_ids = ['djznu', 'dkhgu' ]

 gl = '/nfs/a90/eepdw/Data/EMBRACE/Mean_State/pp_files/djzn/djznw/%s.pp' % pp_file
 glob = iris.load_cube(gl)
 
 for experiment_id in experiment_ids:
 
  expmin1 = experiment_id[:-1]
  pfile = '%s%s/%s/%s.pp' % (pp_file_dir, expmin1, experiment_id, pp_file)

  ofile = '%s%s/%s/33.pp' % (pp_file_dir, expmin1, experiment_id)

 
 
 # Get min and max latitude/longitude and unrotate  to get min/max corners to crop plot automatically - otherwise end with blank bits on the edges 
  oc = iris.load_cube(ofile)

  lats = oc.coord('grid_latitude').points
  lons = oc.coord('grid_longitude').points

  print lons
  
  cs = oc.coord_system('CoordSystem')
  if isinstance(cs, iris.coord_systems.RotatedGeogCS):

      print 'Rotated CS %s' % cs
     
      lon_low= np.min(lons)
      lon_high = np.max(lons)
      lat_low = np.min(lats)
      lat_high = np.max(lats)

      lon_corners, lat_corners = np.meshgrid((lon_low, lon_high), (lat_low, lat_high))
      
      lon_corner_u,lat_corner_u = unrotate.unrotate_pole(lon_corners, lat_corners, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)
      lon_low = lon_corner_u[0,0]
      lon_high = lon_corner_u[0,1]
      lat_low = lat_corner_u[0,0]
      lat_high = lat_corner_u[1,0]

  else: 
      lon_low= np.min(lons)
      lon_high = np.max(lons)
      lat_low = np.min(lats)
      lat_high = np.max(lats)

  lon_low_tick=lon_low -(lon_low%divisor)
  lon_high_tick=math.ceil(lon_high/divisor)*divisor

  lat_low_tick=lat_low - (lat_low%divisor)
  lat_high_tick=math.ceil(lat_high/divisor)*divisor
 
  print lat_high_tick
  print lat_low_tick

 
  plist = iris.load(pfile)

  pcubef=np.empty(oc.shape, np.float32)


  #latitude = iris.coords.DimCoord(oc.coord('grid_latitude').points, standard_name='grid_latitude',
                    #iris.coord_systems.RotatedGeogCS(76.0, 263.0, ellipsoid=iris.coord_systems.GeogCS(6371229.0)))
  #longitude = iris.coords.DimCoord(oc.coord('grid_longitude').points, standard_name='grid_longitude',
                     #iris.coord_systems.RotatedGeogCS(76.0, 263.0, ellipsoid=iris.coord_systems.GeogCS(6371229.0))))


  for pcube in plist:
      armin = np.searchsorted(oc.coord('grid_longitude').points, min(pcube.coord('grid_longitude').points))
      armax = np.searchsorted(oc.coord('grid_longitude').points, max(pcube.coord('grid_longitude').points))
      print armax
      print armin
     
      if (armax+1-armin==pcube.shape[1]):
          pcubef[:,armin:armax+1] = pcube.data
      if (armax-armin==pcube.shape[1]):
          pcubef[:,armin:armax] = pcube.data
      
  pcubef=np.array(pcubef)

 
  print pcubef.shape
                     
  pc = iris.cube.Cube(pcubef,standard_name=pcube.standard_name, units =pcube.units,dim_coords_and_dims=[(oc.coord('grid_latitude'), 0), (oc.coord('grid_longitude'), 1)])
  print pc

  pcubeplot=iris.analysis.maths.multiply(pc,3600)

  plt.figure(figsize=(8,8))
         
  cmap=cm.s3pcpn_l
    
  ax = plt.axes(projection=ccrs.PlateCarree(), extent=(lon_low,lon_high,lat_low+degs_crop_bottom,lat_high-degs_crop_top))
  
  clevs = np.linspace(min_contour, max_contour,256)

  cont = iplt.contourf(pcubeplot, clevs, cmap=cmap, extend='both')
                     
  #plt.clabel(cont, fmt='%d')
  #ax.stock_img()
  ax.coastlines(resolution='110m', color='#262626') 
                     
  gl = ax.gridlines(draw_labels=True,linewidth=0.5, color='#262626', alpha=0.5, linestyle='--')
  gl.xlabels_top = False
  gl.ylabels_right = False

  gl.xlines = True
  gl.ylines = True

  gl.xlocator = mticker.FixedLocator(range(int(lon_low_tick),int(lon_high_tick)+divisor,divisor))
  gl.ylocator = mticker.FixedLocator(range(int(lat_low_tick),int(lat_high_tick)+divisor,divisor))
  gl.xformatter = LONGITUDE_FORMATTER
  gl.yformatter = LATITUDE_FORMATTER
  
  gl.xlabel_style = {'size': 12, 'color':'#262626'}
  #gl.xlabel_style = {'color': '#262626', 'weight': 'bold'}
  gl.ylabel_style = {'size': 12, 'color':'#262626'}         

  cbar = plt.colorbar(cont, orientation='horizontal', pad=0.05, extend='both', format = '%d')
  cbar.set_label('mm/h', fontsize=10) 
  #cbar.set_label(pcube.units, fontsize=10)
  cbar.set_ticks(np.arange(min_contour, max_contour+tick_interval,tick_interval))
  ticks = (np.arange(min_contour, max_contour+tick_interval,tick_interval))
  cbar.set_ticklabels(['%.1f' % i for i in ticks])
  main_title=pcube.standard_name.title().replace('_',' ')
  model_info=re.sub('(.{68}. )', '\\1\n', str(model_name_convert_title.main(experiment_id)), 0, re.DOTALL)
  model_info = re.sub(r'[(\']', ' ', model_info)
  model_info = re.sub(r'[\',)]', ' ', model_info)
  print model_info
 
  if not os.path.exists('%s%s/%s' % (save_path, experiment_id, pp_file)): os.makedirs('%s%s/%s' % (save_path, experiment_id, pp_file))

  plt.savefig('%s%s/%s/%s_%s_notitle.png' % (save_path, experiment_id, pp_file, experiment_id, pp_file), format='png', bbox_inches='tight')

  plt.title('\n'.join(wrap('%s\n%s' % (main_title, model_info), 1000,replace_whitespace=False)), fontsize=16, color='#262626')
  
  #plt.show()
 
  plt.savefig('%s%s/%s/%s_%s.png' % (save_path, experiment_id, pp_file, experiment_id, pp_file), format='png', bbox_inches='tight')
  
  plt.close()

  del pcubef
if __name__ == '__main__':
   main()
