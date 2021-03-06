import cPickle as pickle
import numpy as np

pcp_dom, longitude_dom, latitude_dom, time_dom = pickle.load(open('trmm_emb.p', 'rb'))

# Calculate mean at each lat,lon position

#mean_dom = np.mean(pcp_dom, axis=0)

longitude_domsingle = longitude_dom[1,:]
latitude_domsingle = latitude_dom[1,:]
sum_dom = np.sum(pcp_dom, axis=0)

pickle.dump([sum_dom, latitude_domsingle, longitude_domsingle], open('trmm_emb_pcpsum.p', 'wb'))
