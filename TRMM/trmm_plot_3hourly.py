import matplotlib

#matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
from matplotlib import rc
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
from matplotlib import cm

from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import cm as cm_base

import cPickle as pickle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from matplotlib.patches import Polygon

rc('font', family = 'serif', serif = 'cmr10')
rc('text', usetex=True)

rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True
rcParams['font.family']='serif'
rcParams['font.serif']='cmr10'

import datetime
from dateutil import tz

min_contour = 0
max_contour = 3
tick_interval=0.3                  

lon_high = 102
lon_low = 64
lat_high= 30.
lat_low=-10.5

divisor=10  # for lat/lon rounding

sum_dom, latitude_domsingle, longitude_domsingle, time_dom, hours= pickle.load(open('/nfs/a90/eepdw/Data/Saved_data/TRMM/trmm_emb_pcpmean_by_hour.p', 'rb'))




   # Calculate total at each lat,lon position

#mean_dom = np.mean(pcp_dom, axis=0)

#sum_dom = np.sum(pcp_dom, axis=0)

lon_mid=longitude_domsingle[90]
lat_mid=latitude_domsingle[80]
lons= longitude_domsingle[:]
lats = latitude_domsingle[:]

lons,lats = np.meshgrid(lons, lats)

#lon_0 = -nc.variables['true_lon'].getValue()
#lat_0 = nc.variables['true_lat'].getValue()

# create figure and axes instances
for i,h in enumerate(sum_dom):
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_axes([0.1,0.1,0.8,0.8])

#Convert to India time

    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Asia/Kolkata')

    hours_utc = datetime.datetime(2011,8,1,int(hours[i]), 0, 0, ).replace(tzinfo=from_zone)
    hours_local=hours_utc.astimezone(to_zone).strftime('%H%M')  

    m = Basemap(projection='mill',\
            llcrnrlat=lat_low,urcrnrlat=lat_high,\
            llcrnrlon=lon_low,urcrnrlon=lon_high,\
           rsphere=6371229.,resolution='h',area_thresh=10000)


# draw coastlines, state and country boundaries, edge of map.
    m.drawcoastlines(linewidth=0.5,color='#262626')
#m.drawstates()
    m.drawcountries(linewidth=0.5,color='#262626')
# draw parallels.
    parallels = np.arange(0.,90,divisor)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10, color='#262626')
# draw meridians
    meridians = np.arange(0.,360., divisor)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10, color='#262626')
#ny = mean_dom.shape[0]; nx = mean_dom.shape[1]
#lons, lats = m.makegrid(longitude_dom[1,:], latitude_dom[1,:]) # get lat/lons of ny by nx evenly space grid.
    x, y = m(lons, lats) # compute map proj coordinates.
# draw filled contours.

    clevs = np.linspace(min_contour, max_contour,256)
    ticks = (np.arange(min_contour, max_contour+tick_interval,tick_interval))

    cs = m.contourf(x,y,h, clevs, cmap=cm_base.s3pcpn_l, extend='both')
# add colorbar.
#cbar = m.colorbar(cs,location='bottom',pad="5%")
    cbar = m.colorbar(cs,location='bottom',pad="5%")

    cbar.set_ticklabels(["${%.1f}$" % t for t in ticks])
    cbar.set_label('mm/h')

    if int(hours[i])<10:
        hours[i] = '0%s' % int(hours[i])
        print hours[i]
    plt.savefig('/nfs/a90/eepdw/Figures/TRMM/TRMM_mean_EMBRACE_period_%s_notitle.png' % hours[i], format='png', bbox_inches='tight')

    plt.title('TRMM Rainfall Retrieval Mean at %s00 UTC (%s IST) for EMBRACE Period - 21 days from 21st August 2011' % (hours[i], hours_local), fontsize=16, color='#262626')

    plt.savefig('/nfs/a90/eepdw/Figures/TRMM/TRMM_mean_EMBRACE_period_%s_title.png' % hours[i], format='png', bbox_inches='tight')

    plt.title('%s00 UTC - %s IST' % (hours[i], hours_local), fontsize=16, color='#262626')
    plt.savefig('/nfs/a90/eepdw/Figures/TRMM/TRMM_mean_EMBRACE_period_%s_short_title.png' % hours[i], format='png', bbox_inches='tight')

    #plt.show()
