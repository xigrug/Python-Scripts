"""

Load pp, plot and save


"""

import os, sys


#%matplotlib inline
#%pylab inline

import matplotlib

matplotlib.use('Agg') 
# Must be before importing matplotlib.pyplot or pylab!
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

import pdb

save_path='/nfs/a90/eepdw/Figures/EMBRACE/'

model_name_convert_title = imp.load_source('util', '/nfs/see-fs-01_users/eepdw/python_scripts/modules/model_name_convert_title.py')
unrotate = imp.load_source('util', '/nfs/see-fs-01_users/eepdw/python_scripts/modules/unrotate_pole.py')
#pp_file = ''
plot_diags=['temp', 'sp_hum']
plot_levels = [925, 850, 700, 500] 

experiment_ids = ['dklyu', 'dkmbq']
#experiment_ids = ['djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkbhu', 'djznu', 'dkhgu' ] # All 12


pp_file_path = '/nfs/a90/eepdw/Data/EMBRACE/'


degs_crop_top = 1.7
degs_crop_bottom = 2.5

from iris.coord_categorisation import add_categorised_coord

def add_hour_of_day(cube, coord, name='hour'):
    add_categorised_coord(cube, name, coord,
          lambda coord, x: coord.units.num2date(x).hour)

figprops = dict(figsize=(8,8), dpi=100)

#cmap=cm.s3pcpn_l


u = unit.Unit('hours since 1970-01-01 00:00:00',calendar='gregorian')
dx, dy = 10, 10

divisor=10  # for lat/lon rounding

lon_high = 101.866 
lon_low = 64.115
lat_high = 33.
lat_low =-6.79

lon_low_tick=lon_low -(lon_low%divisor)
lon_high_tick=math.ceil(lon_high/divisor)*divisor

lat_low_tick=lat_low - (lat_low%divisor)
lat_high_tick=math.ceil(lat_high/divisor)*divisor


def main():
  
 
#experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkbhu', 'djznu', 'dkhgu' ] # All 12
 #experiment_ids = ['djzny', 'djzns', 'djznw', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ] 
 #experiment_ids = ['djzny', 'djzns', 'djznu', 'dkbhu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkhgu'] 
 #experiment_ids = ['djzns', 'djznu', 'dkbhu', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkhgu'] 
 #experiment_ids = ['dklzq', 'dkmbq', 'dkjxq', 'dklwu', 'dklyu', 'djzns']
#experiment_ids = ['djzns' ] 
 #experiment_ids = ['dkhgu','dkjxq']
 
    for p_level in plot_levels:

        # Set pressure height contour min/max
        if p_level == 925:
            clevgh_min = -24.
            clevgh_max = 24.
        elif p_level == 850:
            clevgh_min = -24.
            clev_max = 24.
        elif p_level == 700:
            clevgh_min = -24.
            clev_max = 24.
        elif p_level == 500:
            clevgh_min = -24.
            clevgh_max = 24.
        else:
            print 'Contour min/max not set for this pressure level'

# Set potential temperature min/max       
        if p_level == 925:
            clevpt_min = -3.
            clevpt_max = 100.
        elif p_level == 850:
            clevpt_min = -3.
            clevpt_max = 3.
        elif p_level == 700:
            clevpt_min = -3.
            clevpt_max = 3.
        elif p_level == 500:
            clevpt_min = -3.
            clevpt_max = 3.
        else:
            print 'Potential temperature min/max not set for this pressure level'

 # Set specific humidity min/max       
        if p_level == 925:
            clevsh_min = -0.0025
            clevsh_max = 0.0025
        elif p_level == 850:
            clevsh_min = -0.0025
            clevsh_max = 0.0025
        elif p_level == 700:
            clevsh_min = -0.0025
            clevsh_max = 0.0025
        elif p_level == 500:
            clevsh_min = -0.0025
            clevsh_max = 0.0025
        else:
            print 'Specific humidity min/max not set for this pressure level'

        clevs_lin = np.linspace(clevgh_min, clevgh_max, num=24)

        
        p_level_constraint = iris.Constraint(pressure=p_level)

                        
        for plot_diag in plot_diags:
        
        

        

            for experiment_id in experiment_ids:
            
                expmin1 = experiment_id[:-1]

                pp_file = '%s_%s_on_p_levs_mean_by_hour.pp' % (experiment_id, plot_diag)
                pfile = '%s%s/%s/%s' % (pp_file_path, expmin1, experiment_id, pp_file)
                pcube = iris.load_cube(pfile, p_level_constraint)
                #cube=iris.analysis.maths.multiply(pcube,3600)
                # For each hour in cube

                height_pp_file = '%s_408_on_p_levs_mean_by_hour.pp' % (experiment_id)
                height_pfile = '%s%s/%s/%s' % (pp_file_path, expmin1, experiment_id, height_pp_file)
                height_cube = iris.load_cube(height_pfile, p_level_constraint)

                #time_coords = cube_f.coord('time')
                add_hour_of_day(pcube, pcube.coord('time'))
     
                add_hour_of_day(height_cube, height_cube.coord('time'))
    

                    
                #pdb.set_trace()

                #del height_cube, pcube, height_cube_diff, cube_diff

                for t, time_cube in enumerate(pcube.slices(['grid_latitude', 'grid_longitude'])):
                    
                    hour=time_cube.coord('hour').points[0]

                    if hour==23:
                        hour=0

                    #pdb.set_trace()

                    cube_diff_slice = pcube.extract(iris.Constraint(hour=hour+1))
                
                    p_cube_difference = cube_diff_slice - time_cube
                    
                    #pdb.set_trace()
                
                    print time_cube
                    time_cube_408 = height_cube.extract(iris.Constraint(hour=hour))
                    height_cube_diff_slice = height_cube.extract(iris.Constraint(hour=hour+1))
                    
                    height_cube_difference = height_cube_diff_slice -  time_cube_408
                    # Get  time of averagesfor plot title
  

                    h = u.num2date(np.array(time_cube.coord('hour').points, dtype=float)[0]).strftime('%H%M')
                    hplus1 = u.num2date(np.array(time_cube.coord('hour').points, dtype=float)[0]+1.).strftime('%H%M')

                    #Convert to India time

                    from_zone = tz.gettz('UTC')
                    to_zone = tz.gettz('Asia/Kolkata')
                    
                    h_utc = u.num2date(np.array(time_cube.coord('hour').points, dtype=float)[0]).replace(tzinfo=from_zone)
                   
                    h_local = h_utc.astimezone(to_zone).strftime('%H%M')
                
                    fig = plt.figure(**figprops)
         
                    cmap=plt.cm.RdBu_r
                    
                    ax = plt.axes(projection=ccrs.PlateCarree(), extent=(lon_low,lon_high,lat_low+degs_crop_bottom,lat_high-degs_crop_top))
                    
                    m =\
                        Basemap(llcrnrlon=lon_low,llcrnrlat=lat_low,urcrnrlon=lon_high,urcrnrlat=lat_high, rsphere = 6371229)
                    #pdb.set_trace()
                    lat = p_cube_difference.coord('grid_latitude').points
                    lon = p_cube_difference.coord('grid_longitude').points
                    
                    cs = p_cube_difference.coord_system('CoordSystem')
                    
                    lons, lats = np.meshgrid(lon, lat) 
                    lons, lats = iris.analysis.cartography.unrotate_pole\
                                (lons,lats, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)
                    
                    
                    x,y = m(lons,lats)
                    
                    
                    if plot_diag=='temp':
                        min_contour = clevpt_min
                        max_contour = clevpt_max
                        cb_label='K' 
                        main_title='geopotential height (grey contours), potential temperature (colours),\
                                          and wind (vectors) %s UTC    %s IST' % (h, h_local)
                        tick_interval=1
                    elif plot_diag=='sp_hum':
                        min_contour = clevsh_min
                        max_contour = clevsh_max 
                        cb_label='kg/kg' 
                        main_title='8km  Explicit model (dklyu) minus 8km parametrised model geopotential height (grey contours), specific humidity (colours),\
                                         and wind (vectors) %s-%s UTC    %s-%s IST' % (h, h_local)
                        tick_interval=0.0005
                        
                    clevs = np.linspace(min_contour, max_contour, 32)
                    clevs = np.linspace(-3, 3, 32)
                    cont = plt.contourf(x,y,p_cube_difference.data, clevs, cmap=cmap, extend='both')
                    
                    
                    #cont = iplt.contourf(time_cube, cmap=cmap, extend='both')
                    

                    cs_lin = iplt.contour(height_cube_difference, clevs_lin,colors='#262626',linewidths=1.)
                    plt.clabel(cs_lin, fontsize=14, fmt='%d', color='black')
                    
                    #del time_cube
                     
                    #plt.clabel(cont, fmt='%d')
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
                    cbar.set_label('%s' % cb_label, fontsize=10, color='#262626') 
                    #cbar.set_label(time_cube.units, fontsize=10, color='#262626')
                    cbar.set_ticks(np.arange(min_contour, max_contour+tick_interval,tick_interval))
                    ticks = (np.arange(min_contour, max_contour+tick_interval,tick_interval))
                    cbar.set_ticklabels(['${%.1f}$' % i for i in ticks])
                    
                    cbar.ax.tick_params(labelsize=10, color='#262626')
                    
                    
                    #main_title='Mean Rainfall for EMBRACE Period -%s UTC (%s IST)' % (h, h_local)
                    #main_title=time_cube.standard_name.title().replace('_',' ')
                    #model_info = re.sub(r'[(\']', ' ', model_info)
                    #model_info = re.sub(r'[\',)]', ' ', model_info)
                    #print model_info
                    
                    file_save_name = '%s_%s_%s_hour_%s_diff_from_%s' % (experiment_id, plot_diag, p_level, hplus1, h)
                    save_dir = '%s%s/%s' % (save_path, experiment_id, plot_diag)
                    if not os.path.exists('%s' % save_dir): os.makedirs('%s' % (save_dir))
                    
                    #plt.show()

                    fig.savefig('%s/%s_notitle.png' % (save_dir, file_save_name), format='png', bbox_inches='tight')
                    
                    
                    plt.title('%s UTC %s IST' % (h, h_local))
                    fig.savefig('%s/%s_short_title.png' % (save_dir, file_save_name) , format='png', bbox_inches='tight')
                    
                    
                    #model_info=re.sub('(.{68} )', '\\1\n', str(model_name_convert_title.main(experiment_id)), 0, re.DOTALL)
                    #plt.title('\n'.join(wrap('%s\n%s' % (main_title, model_info), 1000,replace_whitespace=False)), fontsize=16)               
                    #fig.savefig('%s/%s.png' % (save_dir, file_save_name), format='png', bbox_inches='tight')
 
                    fig.clf()
                    plt.close()
                    #del time_cube
                    gc.collect()


if __name__ == '__main__':
   main()
    #proc=mp.Process(target=worker)
    #proc.daemon=True
    #proc.start()
    #proc.join()
