# -*- coding: utf-8 -*-
"""
Created on Thu May 02 17:15:06 2013
@author: Vasya

.... depreciated.... 
whitening, clustering ets 
... whitening and cosine distance do not mix if the vectors aere of a different length

d2_out - dict brands ->LDA vectors
np_out - dict brand  ->number of posts used in LAD vector
"""

import matplotlib.pyplot as plt
import pickle
import scipy
import scipy.linalg
import numpy
import Pycluster

with open('d2_out','r') as file1: d2=pickle.load(file1)
with open('np_out','r') as file1: np=pickle.load(file1)

goodBbands = [b for b in np.keys() if np[b]>500 and b !="Ram"]
d3 = {b:d2[b] for b in goodBbands}
data = numpy.array([d2[b] for b in goodBbands]).squeeze()


ave = numpy.mean(d3.values(),axis=0)
stds=  numpy.std(d3.values(),axis=0)

sims = scipy.zeros((len(goodBbands),len(goodBbands)))
dists =scipy.zeros((len(goodBbands),len(goodBbands)))
 

idx = Pycluster.kcluster(data,3,npass=1)[0]
keys = [goodBbands[i] for i in numpy.argsort(idx)]


for (ia,a) in enumerate(keys):
    for (ib,b) in enumerate(keys):
        v1=(d3[a]-ave)/stds
        v2=(d3[b]-ave)/stds      
        sims[ia,ib]=(v1.T.dot(v2))/(scipy.linalg.norm(v1)*scipy.linalg.norm(v2))
        dists[ia,ib]=scipy.linalg.norm(v1-v2) 

labels = zip([str(t) for t in idx[numpy.argsort(idx)]],keys)
fig = plt.figure()
ax = fig.add_subplot(111)
imgplot = ax.imshow(sims,interpolation='none')
ax.set_yticks(xrange(len(keys)))
ax.set_yticklabels(labels)
 
ax.set_xticks(xrange(len(keys)))
ax.set_xticklabels([t for t in idx[numpy.argsort(idx)]])
plt.colorbar(imgplot)
plt.show()

##
'''
import csv
with open("dists.csv", 'w') as f:
    writer = csv.writer(f)
    for b in xrange(len(goodBbands)):
        sv = dists[b,:]
        writer.writerow(sv)
'''