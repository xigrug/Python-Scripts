"""

Load npy xy, plot and save


"""

import os, sys

import matplotlib

matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!

import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm

from matplotlib import rc
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
from matplotlib import cm

rc('text', usetex=True)

rcParams['text.usetex']=True
rcParams['text.latex.unicode']=True

rc('font', family = 'serif', serif = 'cmr10')

import numpy as np

from datetime import timedelta
import datetime

import imp

import re
from textwrap import wrap

model_name_convert_legend = imp.load_source('util', '/nfs/see-fs-01_users/eepdw/python_scripts/modules/model_name_convert_legend.py')
#unrotate = imp.load_source('util', '/home/pwille/python_scripts/modules/unrotate_pole.py')

pp_file = 'avg.5216'

# Make own time x-axis

d = matplotlib.dates.drange(datetime.datetime(2011, 8, 21, 6,30), datetime.datetime(2011, 8, 22, 6, 30), timedelta(hours=1))

formatter = matplotlib.dates.DateFormatter('%H:%M')

print d

#times = matplotlib.dates.date2num(d)

top_dir='/nfs/a90/eepdw/Mean_State_Plot_Data/Rain_Land_Sea'

def main():
 #experiment_ids = ['djznw', 'djzny', 'djznq', 'djzns', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq', 'dkbhu', 'djznu', 'dkhgu' ] # All 12
 experiment_ids_p = ['djznw', 'djzny', 'djznq', 'dklzq', 'dkmbq' ] # Most of Params
 experiment_ids_e = ['dklwu', 'dklyu', 'djzns', 'dkbhu', 'djznu' ] # Most of Explicit
#experiment_ids = ['djzny', 'djznq', 'djzns', 'djznw', 'dkjxq', 'dklyu', 'dkmbq', 'dklwu', 'dklzq' ] 

 #plt.ion()

 NUM_COLOURS = 9
 cmap=cm.get_cmap(cm.Set1, NUM_COLOURS)
 #cgen = (cmap(1.*i/NUM_COLORS) for i in range(NUM_COLORS))

 for ls in ['land', 'sea']:
  plt.figure(figsize=(12,6))
  linewidth_p=0.2

  legendEntries=[]
  legendtext=[]

  c1=0
  for c, experiment_id in enumerate(experiment_ids_p):

   expmin1 = experiment_id[:-1]
  
   try:
      plotnp = np.load('%s/%s/%s/%s_%s_rainfall_diurnal_np.npy' % (top_dir, expmin1, experiment_id, pp_file, ls))

      if (c<8):
          colour = cmap(1.*c/NUM_COLOURS)
      else:
          c1=c1+1

      if (experiment_id=='dkmbq'):
          print experiment_id
          colour = cmap(1.*8/NUM_COLOURS)
      if (experiment_id=='dklzq'):
          print experiment_id
          colour = cmap(1.*9/NUM_COLOURS)

      #plotnp = np.sort(pnp, axis=1)
      l, = plt.plot_date(d, plotnp[0], label=model_name_convert_legend.main(experiment_id), linewidth=linewidth_p, linestyle='--', marker='', markersize=2, fmt='', color=colour)

      legendEntries.append(l)
      legendtext.append('%s' % (model_name_convert_legend.main(experiment_id)))
      
      linewidth_p=linewidth_p+0.5
    
   except Exception, e:
      print e
      pass

  l1=plt.legend(legendEntries, legendtext, title='Parametrised', loc=9, frameon=False, prop={'size':8}, bbox_to_anchor=(0, 0,1, 1))


  linewidth_exp=0.2

  legendEntries=[]
  legendtext=[]
 
  c1=0
  for c, experiment_id in enumerate(experiment_ids_e):

   expmin1 = experiment_id[:-1]

   try:
      plotnp = np.load('%s/%s/%s/%s_%s_rainfall_diurnal_np.npy' % (top_dir, expmin1, experiment_id, pp_file, ls))

      if (c<8):
          colour = cmap(1.*c/NUM_COLOURS)
      else:
          c1=c1+1

      if (experiment_id=='dklyu'):
          print experiment_id
          colour = cmap(1.*8/NUM_COLOURS)
      if (experiment_id=='dklwu'):
          print experiment_id
          colour = cmap(1.*9/NUM_COLOURS)

      #plotnp = np.sort(pnp, axis=1)
      l, = plt.plot_date(d, plotnp[0], label='%s' % (model_name_convert_legend.main(experiment_id)), linewidth=linewidth_exp, linestyle='-', marker='', markersize=2, fmt='', color=colour)

      legendEntries.append(l)
      legendtext.append('%s' % (model_name_convert_legend.main(experiment_id)))
      linewidth_exp=linewidth_exp+0.5
      #print linewidth_exp

   except Exception, e:
      print e
      pass
  l2=plt.legend(legendEntries, legendtext, title='Explicit', loc=9, frameon=False, bbox_to_anchor=(0.11, 0,1, 1), prop={'size':8})
  plt.gca().add_artist(l1)

  plt.gca().xaxis.set_major_formatter(formatter)

  plt.xlabel('Time (UTC)')
  plt.ylabel('kg/m^2/s')

  title="Domain Averaged Rainfall - %s" % ls

  t=re.sub('(.{68} )', '\\1\n', str(title), 0, re.DOTALL)
  t = re.sub(r'[(\']', ' ', t)
  t = re.sub(r'[\',)]', ' ', t)
  
  
  plt.title('\n'.join(wrap('%s' % (t.title()), 1000,replace_whitespace=False)), fontsize=16)
  #plt.show()

  if not os.path.exists('/nfs/a90/eepdw/Rainfall_plots/Figures/Diurnal/'): os.makedirs('/nfs/a90/eepdw/Rainfall_plots/Figures/Diurnal/')
  plt.savefig('/nfs/a90/eepdw/Rainfall_plots/Figures/Diurnal/%s_%s.png' % (pp_file, ls), format='png', bbox_inches='tight')
  plt.close()


if __name__ == '__main__':
   main()

   
       



