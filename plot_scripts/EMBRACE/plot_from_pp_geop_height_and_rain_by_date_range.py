"""

Load pp, plot and save
8km difference

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

pp_file_contourf = 'rain_mean_by_date_range'
pp_file_contour ='408'
#plot_diags=['sp_hum']

plot_levels = [925] 

#experiment_ids = ['dkmbq', 'dklyu']
experiment_ids = ['dklyu', 'dkmbq', 'djzny', 'djznw', 'djznq', 'djzns', 'dklwu', 'dklzq'] # All minus large 2

cb_label='mm'

min_contour=0.
max_contour=3.
tick_interval=0.3

clevs = np.linspace(min_contour, max_contour,64)

#cmap=plt.cm.jet
cmap=cm.s3pcpn_l

ticks = (np.arange(min_contour, max_contour+tick_interval,tick_interval))


pp_file_path = '/nfs/a90/eepdw/Data/EMBRACE/'

degs_crop_top = 1.7
degs_crop_bottom = 2.5

from iris.coord_categorisation import add_categorised_coord

# def add_hour_of_day(cube, coord, name='hour'):
#     add_categorised_coord(cube, name, coord,
#           lambda coord, x: coord.units.num2date(x).hour)

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
 
    for p_level in plot_levels:

        # Set pressure height contour min/max
        if p_level == 925:
            clev_min = 660.
            clev_max = 810.
        elif p_level == 850:
            clev_min = 1435.
            clev_max = 1530.
        elif p_level == 700:
            clev_min = 3090.
            clev_max = 3155.
        elif p_level == 500:
            clev_min = 5800.
            clev_max = 5890.
        else:
            print 'Contour min/max not set for this pressure level'

       

        #clevs_col = np.arange(clev_min, clev_max)
        clevs_lin = np.arange(clev_min, clev_max, 5)    

        p_level_constraint = iris.Constraint(pressure=p_level)      

        #for plot_diag in plot_diags:    

        for experiment_id in experiment_ids:
            
                expmin1 = experiment_id[:-1]
                pfile = '/nfs/a90/eepdw/Data/EMBRACE/%s/%s/%s_%s.pp' % (expmin1, experiment_id, experiment_id, pp_file_contourf)

                #pc =  iris(pfile)
                pcube_contourf = iris.load_cube(pfile)
                pcube_contourf=iris.analysis.maths.multiply(pcube_contourf,3600)


                height_pp_file = '%s_%s_on_p_levs_mean_by_date_range.pp' % (experiment_id, pp_file_contour)
                height_pfile = '%s%s/%s/%s' % (pp_file_path, expmin1, experiment_id, height_pp_file)
                pcube_contour = iris.load_cube(height_pfile, p_level_constraint)
                

                time_coords = pcube_contourf.coord('time')
                iris.coord_categorisation.add_day_of_year(pcube_contourf, time_coords, name='day_of_year')

                time_coords = pcube_contour.coord('time')
                iris.coord_categorisation.add_day_of_year(pcube_contour, time_coords, name='day_of_year')


                for t, time_cube in enumerate(pcube_contourf.slices(['grid_latitude', 'grid_longitude'])):
                                   
                    #height_cube_slice = pcube_contour.extract(iris.Constraint(day_of_year=time_cube.coord('day_of_year').points))
                    height_cube_slice = pcube_contour[t]

                    #pdb.set_trace()
                    
                    # Get  time of averagesfor plot title
  

                    h = u.num2date(np.array(time_cube.coord('time').points, dtype=float)[0]).strftime('%d%b')

                    #Convert to India time

                    from_zone = tz.gettz('UTC')
                    to_zone = tz.gettz('Asia/Kolkata')
                    
                    h_utc = u.num2date(np.array(time_cube.coord('day_of_year').points, dtype=float)[0]).replace(tzinfo=from_zone)
                   
                    h_local = h_utc.astimezone(to_zone).strftime('%H%M')
                
                    fig = plt.figure(**figprops)
         
                    #cmap=plt.cm.RdBu_r
                    
                    ax = plt.axes(projection=ccrs.PlateCarree(), extent=(lon_low,lon_high,lat_low+degs_crop_bottom,lat_high-degs_crop_top))
                    
                    m =\
                        Basemap(llcrnrlon=lon_low,llcrnrlat=lat_low,urcrnrlon=lon_high,urcrnrlat=lat_high, rsphere = 6371229)
                    # #pdb.set_trace()
                    # lat = pcube_contourf.coord('grid_latitude').points
                    # lon = pcube_contourf.coord('grid_longitude').points
                    
                    # cs = cube.coord_system('CoordSystem')
                    
                    # lons, lats = np.meshgrid(lon, lat) 
                    # lons, lats = iris.analysis.cartography.unrotate_pole\
                    #             (lons,lats, cs.grid_north_pole_longitude, cs.grid_north_pole_latitude)
                    
                    
                    # x,y = m(lons,lats)
                    
                    
                    # if plot_diag=='temp':
                    #     min_contour = clevpt_min
                    #     max_contour = clevpt_max
                    #     cb_label='K' 
                    #     main_title='8km  Explicit model (dklyu) minus 8km parametrised model geopotential height (grey contours), potential temperature (colours),\
                    #                       and wind (vectors) %s UTC    %s IST' % (h, h_local)
                    #     tick_interval=2
                    #     clev_number=max_contour-min_contour+1
                    # elif plot_diag=='sp_hum':
                    #     min_contour = clevsh_min
                    #     max_contour = clevsh_max 
                    #     cb_label='kg/kg' 
                    #     main_title='8km  Explicit model (dklyu) minus 8km parametrised model geopotential height (grey contours), specific humidity (colours),\
                    #                      and wind (vectors) %s UTC    %s IST' % (h, h_local)
                    #     tick_interval=0.002
                    #     clev_number=max_contour-min_contour+0.001

                    # clevs = np.linspace(min_contour, max_contour, clev_number)
                    # #clevs = np.linspace(-3, 3, 32)
                    # cont = plt.contourf(x,y,time_cube.data, clevs, cmap=cmap, extend='both')
                    
                    
                    cont = iplt.contourf(time_cube, clevs, cmap=cmap, extend='both')
                    
                    #pdb.set_trace()
                    cs_lin = iplt.contour(height_cube_slice, clevs_lin,colors='#262626',linewidths=1.)
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
                    
                    # cbar = fig.colorbar(cont, orientation='horizontal', pad=0.05, extend='both')
                    # cbar.set_label('%s' % cb_label, fontsize=10, color='#262626') 
                    # #cbar.set_label(time_cube.units, fontsize=10, color='#262626')
                    # cbar.set_ticks(np.arange(min_contour, max_contour+tick_interval,tick_interval))
                    # ticks = (np.arange(min_contour, max_contour+tick_interval,tick_interval))
                    # cbar.set_ticklabels(['${%.1f}$' % i for i in ticks])
                    
                    # cbar.ax.tick_params(labelsize=10, color='#262626')
                    
                    
                    #main_title='Mean Rainfall for EMBRACE Period -%s UTC (%s IST)' % (h, h_local)
                    #main_title=time_cube.standard_name.title().replace('_',' ')
                    #model_info = re.sub(r'[(\']', ' ', model_info)
                    #model_info = re.sub(r'[\',)]', ' ', model_info)
                    #print model_info
                    
                    file_save_name = '%s_%s_and_%s_%s_hPa_and_geop_height_%s' % (experiment_id, pp_file_contour, pp_file_contourf, p_level, h)
                    save_dir = '%s%s/%s_and_%s' % (save_path, experiment_id, pp_file_contour, pp_file_contourf)
                    if not os.path.exists('%s' % save_dir): os.makedirs('%s' % (save_dir))
                    
                    #plt.show()

                    #fig.savefig('%s/%s_notitle.png' % (save_dir, file_save_name), format='png', bbox_inches='tight')
                    
                    
                    plt.title('%s UTC' % (h))
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





