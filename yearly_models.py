# -*- coding: utf-8 -*-
"""
calibrates LDA models year by year and saves resutls to a folder
uses data from default folder 

improvement - generate a common starting model/dictionary and then update the
basic model using the data from specific year - this way if topic drift is 
small then the topics will be ordered in a similar way throghout all years


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
 
    # this indeed returns a model name string                                       
    modelName= docs2LDAmodel.main(outdir,num_passes, num_topics, threadChoseStr,
                      modelTag,time_low_cutoff,time_hi_cutoff)
                      
    getLikes.main(outdir,modelName,world_list_file_name= "adjectives.txt")
