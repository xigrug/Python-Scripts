import cPickle as pickle
import numpy as np

pcp_dom, longitude_dom, latitude_dom, time_dom, time_hour = pickle.load(open('/nfs/a90/eepdw/Data/Saved_data/TRMM/trmm_emb.p', 'rb'))

# Calculate mean at each lat,lon position

#mean_dom = np.mean(pcp_dom, axis=0)

longitude_domsingle = longitude_dom[1,:]
latitude_domsingle = latitude_dom[1,:]

###############################

## Need to check time interval - TRMM data in 3 hourly intervals, given in mm/hr
############################

time_interval=3

sum_dom = np.sum(pcp_dom*time_interval, axis=0)

#pickle.dump([mean_dom, latitude_domsingle, longitude_domsingle], open('/nfs/see-fs-01_users/eepdw/Saved_data/TRMM/trmm_emb_pcpmean.p', 'wb'))

pickle.dump([sum_dom, latitude_domsingle, longitude_domsingle], open('/nfs/see-fs-01_users/eepdw/Saved_data/TRMM/trmm_emb_pcpsum.p', 'wb'))
