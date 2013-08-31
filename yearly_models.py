# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 20:28:43 2013

@author: Vasya
"""
import docs2LDAmodel
import time
import getLikes
import os

num_topics=20
num_passes=2
threadChoseStr=''

for year in ["2003","2004",'2006','2007','2008']: 
    outdir = r'Z:\ermunds\results\\' + year +" "+ str(num_topics) +'topics'
    os.mkdir(outdir)
    modelTag=year+" "
    time_low_cutoff=time.strptime("1 Jan " + year, "%d %b %Y")
    time_hi_cutoff=time.strptime( "31 Dec "+ year, "%d %b %Y")                                         
    modelName= docs2LDAmodel.main(outdir,num_passes, num_topics, threadChoseStr,
                      modelTag,time_low_cutoff,time_hi_cutoff)
    getLikes.main(outdir,modelName,world_list_file_name= "adjectives.txt")
