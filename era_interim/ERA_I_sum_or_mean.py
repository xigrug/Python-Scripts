import cPickle as pickle
import numpy as np

#variables_list=['sphum', 'geopotential', 'u_wind', 'v_wind', 'cloud_cover', 'temperature']
variables_list=['temperature']
###############################

## Need to check time interval - TRMM data in 3 hourly intervals, given in mm/hr, ERA-I in 6 hourly
############################

time_interval=6

for v in variables_list:

 variable_dom, longitude_dom, latitude_dom, time_dom, time_hour = pickle.load(open('/nfs/a90/eepdw/Data/Saved_data/era_i/era_i_emb_time_update_large_%s.p' % v, 'rb'))

# Calculate potential temperature for air temperature 

 gas_constant_of_air_over_constant_pressure_process = 0.286
 if v=='temperature':
     pressure_levels =  pickle.load(open('/nfs/a90/eepdw/Data/Saved_data/era_i/era_i_emb_pressure_levels.p', 'rb'))
     gas_constant_of_air_over_constant_pressure_process = 0.286
     for i in range(variable_dom.shape[1]):
         variable_dom[:,i,:,:] = variable_dom[:,i,:,:]*((1000./pressure_levels[i])**gas_constant_of_air_over_constant_pressure_process)

 #sum_dom = np.sum(variable_dom*time_interval, axis=0)
# Calculate mean at each lat,lon position

 mean_dom = np.mean(variable_dom, axis=0, dtype=np.float64)
 longitude_domsingle = longitude_dom[1,:]
 latitude_domsingle = latitude_dom[1,:]

###############################

## Need to check time interval - TRMM data in 3 hourly intervals, given in mm/hr
############################

 
 pickle.dump([mean_dom, latitude_domsingle, longitude_domsingle], open('/nfs/a90/eepdw/Data/Saved_data/era_i/era_i_emb_%s_mean.p' % v, 'wb'))

 #pickle.dump([sum_dom, latitude_domsingle, longitude_domsingle], open('/nfs/a90/eepdw/Data/Saved_data/era_i/era_i_emb_%s_sum.p' % v, 'wb'))
