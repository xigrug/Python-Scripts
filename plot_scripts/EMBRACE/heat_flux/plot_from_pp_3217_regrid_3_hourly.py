"""

Load pp, plot and save


"""

import os, sys

import matplotlib

#matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
from matplotlib import rc
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams

from mpl_toolkits.basemap import Basemap

rc('font', family = 'serif', serif = 'cmr10')
rc('text', usetex=True)

rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True
rcParams['font.family']='serif'
rcParams['font.serif']='cmr10'

import matplotlib.pyplot as plt
#from matplotlib import figure
import matplotlib as mpl
import matplotlib.cm as mpl_cm
import numpy as np

import iris
import iris.coords as coords
import iris.quickplot as qplt
import iris.plot as iplt
import iris.coord_categorisation
import iris.unit as unit

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

from dateutil import tz

#import multiprocessing as mp

import gc

import types

save_path='/nfs/a90/eepdw/Figures/EMBRACE/'

model_name_convert_title = imp.load_source('util', '/nfs/see-fs-01_users/eepdw/python_scripts/modules/model_name_convert_title.py')
unrotate = imp.load_source('util', '/nfs/see-fs-01_users/eepdw/python_scripts/modules/unrotate_pole.py')
pp_file = '3217_mean_by_hour_regrid'

degs_crop_top = 1.7
degs_crop_bottom = 2.5

min_contour = 0
max_contour = 200
tick_interval=20

figprops = dict(figsize=(8,8), dpi=360)


clevs = np.linspace(min_contour, max_contour,32)

#cmap=cm.s3pcpn_l

ticks = (np.arange(min_contour, max_contour+tick_interval,tick_interval))
u = unit.Unit('hours since 1970-01-01 00:00:00',calendar='gregorian')
dx, dy = 10, 10

divisor=10  # for lat/lon rounding

def main():
 experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkbhu', 'djznu', 'dkhgu' ] # All 12
 #experiment_ids = ['djzny', 'djzns', 'djznw', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ] 
 #experiment_ids = ['djzny', 'djzns', 'djznu', 'dkbhu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkhgu'] 
 #experiment_ids = ['djzns', 'djznu', 'dkbhu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkhgu'] 
 #experiment_ids = ['dklzq', 'dkmbq', 'dkjxq', 'dklwu', 'dklyu', 'djzns']
#experiment_ids = ['djzns' ] 
 #experiment_ids = ['dkhgu','dkjxq']

 for experiment_id in experiment_ids:
  
  model_info=re.sub('(.{68} )', '\\1\n', str(model_name_convert_title.main(experiment_id)), 0, re.DOTALL)
  expmin1 = experiment_id[:-1]
  pfile = '/nfs/a90/eepdw/Data/EMBRACE/Mean_State/pp_files/%s/%s/%s.pp' % (expmin1, experiment_id, pp_file)

     #pc =  iris(pfile)
  pcube = iris.load_cube(pfile)
  #pcube=iris.analysis.maths.multiply(pcube,3600)
# For each hour in cube


 # Get min and max latitude/longitude and unrotate  to get min/max corners to crop plot automatically - otherwise end with blank bits on the edges 
  lats = pcube.coord('grid_latitude').points
  lons = pcube.coord('grid_longitude').points
  
  cs = pcube.coord_system('CoordSystem')
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

  #lon_low= 62
  #lon_high = 102
  #lat_low = -7
  #lat_high = 33

  #lon_high_box = 101.866 
  #lon_low_box = 64.115
  #lat_high_box = 33.
  #lat_low_box =-6.79

  lon_high = 101.866 
  lon_low = 64.115
  lat_high = 33.
  lat_low =-6.79

  lon_low_tick=lon_low -(lon_low%divisor)
  lon_high_tick=math.ceil(lon_high/divisor)*divisor

  lat_low_tick=lat_low - (lat_low%divisor)
  lat_high_tick=math.ceil(lat_high/divisor)*divisor
 
  print lat_high_tick
  print lat_low_tick
  for t, time_cube in enumerate(pcube.slices(['grid_latitude', 'grid_longitude'])):

   
   print time_cube
    
   # Get mid-point time of averages
  

   h_max = u.num2date(time_cube.coord('time').bounds[0].max()).strftime('%H%M')
   h_min = u.num2date(time_cube.coord('time').bounds[0].min()).strftime('%H%M')

#Convert to India time

   from_zone = tz.gettz('UTC')
   to_zone = tz.gettz('Asia/Kolkata')

   h_max_utc = u.num2date(time_cube.coord('time').bounds[0].max()).replace(tzinfo=from_zone)
   h_min_utc = u.num2date(time_cube.coord('time').bounds[0].min()).replace(tzinfo=from_zone)

   h_max_local = h_max_utc.astimezone(to_zone).strftime('%H%M')
   h_min_local = h_min_utc.astimezone(to_zone).strftime('%H%M')

#m = u.num2date(time_cube.coord('time').bounds[0].mean()).minute
   #h = u.num2date(time_cube.coord('time').bounds[0].mean()).hour

   #if t==0:
   fig = plt.figure(**figprops)
         
   cmap=plt.cm.YlOrRd
   ax = plt.axes(projection=ccrs.PlateCarree(), extent=(lon_low,lon_high,lat_low+degs_crop_bottom,lat_high-degs_crop_top))
  
  #ax = fig.axes(projection=ccrs.PlateCarree(), extent=(lon_low,lon_high,lat_low,lat_high))

  #ax = fig.axes(projection=ccrs.PlateCarree())

   cont = iplt.contourf(time_cube, clevs, cmap=cmap, extend='both')

   #del time_cube
                     
  #fig.clabel(cont, fmt='%d')
  #ax.stock_img()
   ax.coastlines(resolution='110m', color='#262626') 
                     
   gl = ax.gridlines(draw_labels=True,linewidth=0.5, color='#262626', alpha=0.5, linestyle='--')
   gl.xlabels_top = False
   gl.ylabels_right = False
            #gl.xlines = False
   dx, dy = 10, 10

   gl.xlocator = mticker.FixedLocator(range(int(lon_low_tick),int(lon_high_tick)+dx,dx))
   gl.ylocator = mticker.FixedLocator(range(int(lat_low_tick),int(lat_high_tick)+dy,dy))
   gl.xformatter = LONGITUDE_FORMATTER
   gl.yformatter = LATITUDE_FORMATTER
  
   gl.xlabel_style = {'size': 12, 'color':'#262626'}
  #gl.xlabel_style = {'color': '#262626', 'weight': 'bold'}
   gl.ylabel_style = {'size': 12, 'color':'#262626'}         

   cbar = fig.colorbar(cont, orientation='horizontal', pad=0.05, extend='both')
   cbar.set_label('mm/h', fontsize=10, color='#262626') 
  #cbar.set_label(time_cube.units, fontsize=10, color='#262626')
   cbar.set_ticks(np.arange(min_contour, max_contour+tick_interval,tick_interval))
   cbar.set_ticklabels(['${%.1f}$' % i for i in ticks])
   cbar.ax.tick_params(labelsize=10, color='#262626')

 #   fig.canvas.draw()
  #  background = fig.canvas.copy_from_bbox(fig.bbox)

  
 #   fig = plt.figure(frameon=False,**figprops)
      # make sure frame is off, or everything in existing background
      # will be obliterated.
 #   ax = fig.add_subplot(111,frameon=False)
# restore previous background.
 #   fig.canvas.restore_region(background)

  #  time_cube=iris.analysis.maths.multiply(time_cube,3600)
  #  cont = iplt.contourf(time_cube, clevs, cmap=cmap, extend='both')
    
 #print cont.collections()
   #################################################################
    ## Bug fix for Quad Contour set not having attribute 'set_visible'

      # def setvisible(self,vis):
    #       for c in self.collections: c.set_visible(vis)
     #  cont.set_visible = types.MethodType(setvisible,)
     #  cont.axes = plt.gca()
     #  cont.figure=fig
    ####################################################################

   #ims.append([im])

   
   main_title='Mean Rainfall for EMBRACE Period -%s-%s UTC (%s-%s IST)' % (h_min, h_max, h_min_local, h_max_local)
  #main_title=time_cube.standard_name.title().replace('_',' ')
  #model_info = re.sub(r'[(\']', ' ', model_info)
  #model_info = re.sub(r'[\',)]', ' ', model_info)
  #print model_info

   if not os.path.exists('%s%s/%s' % (save_path, experiment_id, pp_file)): os.makedirs('%s%s/%s' % (save_path, experiment_id, pp_file))

   #fig.show()

   fig.savefig('%s%s/%s/%s_%s_%s-%s_notitle.png' % (save_path, experiment_id, pp_file, experiment_id, pp_file, h_min, h_max), format='png', bbox_inches='tight')

   plt.title('%s-%s UTC    %s-%s IST' % (h_min,h_max, h_min_local, h_max_local))

   fig.savefig('%s%s/%s/%s_%s_%s-%s_short_title.png' % (save_path, experiment_id, pp_file, experiment_id, pp_file, h_min, h_max), format='png', bbox_inches='tight')

   plt.title('\n'.join(wrap('%s\n%s' % (main_title, model_info), 1000,replace_whitespace=False)), fontsize=16)
  
   fig.savefig('%s%s/%s/%s_%s_%s-%s.png' % (save_path, experiment_id, pp_file, experiment_id, pp_file, h_min, h_max), format='png', bbox_inches='tight')
 
   fig.clf()
   plt.close()
   del time_cube
   gc.collect()


if __name__ == '__main__':
   main()
    #proc=mp.Process(target=worker)
    #proc.daemon=True
    #proc.start()
    #proc.join()
