# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 22:01:58 2013

@author: Vasya
"""
import genSimLDAlib as gslib
import numpy as np
import os

def sparse2vectorArrgerator(spVec,agg):
    for i,value in spVec:
        agg[i]+=value
        
def marginal_topic_distribution(lda,mm):
    agg = np.zeros(lda.num_topics)
    for i in xrange(len(mm)-1) :
        sparse2vectorArrgerator(lda[mm[i+1]],agg)
    return agg/agg.sum()
    
def compute_and_save(modelName="201220topics", LDAdir=r"Z:\ermunds\results\2012 20topics"): 
    dirs = gslib.LDAdirs(indir=LDAdir,modelName=modelName)
    (_,mm,lda)=gslib.loadStuff(dirs)    
    agg = marginal_topic_distribution(lda,mm)
    np.savetxt( os.path.join(LDAdir,"topics_marginal.csv"), agg, delimiter=",")
    return agg