# -*- coding: utf-8 -*-
"""
Created on Wed Aug 07 21:40:10 2013

@author: Vasya
"""

import getLikes

import numpy as np
import genSimLDAlib as gslib
import mess_with_sims





indir=r"Z:\ermunds\results\2005 20topics"
modelName="2005+20topics"
    
dirs = gslib.LDAdirs(modelName,indir)
(dict1,_,lda)=gslib.loadStuff(dirs)

words = mess_with_sims.BrandsClustered_1
#words = lda.id2word.values()
wordsClean = getLikes.pruneWordsList(words,lda)

weights = getLikes.LDAweights(lda,wordsClean["IDs"])

import matplotlib.pyplot as plt


yy = wordsClean.Counts
xx = np.sqrt(weights)
labels = wordsClean.index

plt.scatter(xx,yy, marker='.')
'''
for label, x, y in zip(labels, xx, yy):
    plt.annotate(
        label, 
        xy = (x, y), xytext = (-20, 20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
plt.show()
'''