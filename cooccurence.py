# -*- coding: utf-8 -*-
"""
Created on Tue May 14 00:10:36 2013

@author: Vasya
"""
import numpy
import gensim
import genSimLDAlib as gslib
#import someBrandFiltering as bf
import ldaModel2WD as wd
import sims_csv_plotter as draw
import mess_with_sims as sims



#dirs = gslib.LDAdirs(indir=r"Z:\ermunds\results\all unbranded threads",    modelName="unbranded2passes_20topics")
dirs = gslib.LDAdirs(indir=r"Z:\ermunds\results\sink",    modelName="unbranded220topics")

dict1 = gensim.corpora.dictionary.Dictionary().load(dirs.dictFileName)
mm=gensim.corpora.MmCorpus(dirs.corpusFname)

#raw_brands = bf.getMakes();
raw_brands=sims.BrandsClustered_1
brandsl,IDl,ID2index = gslib.world_list2IDs(dict1,raw_brands,tokenizef=gslib.wordCleanUp)

l_1=len(IDl)
l_2=len(IDl)
IDset_1=set(IDl)
IDset_2=set(IDl)
ID2index_1=ID2index
ID2index_2=ID2index

counter_1 = numpy.zeros((1,l_1))
counter_2 = numpy.zeros((1,l_2))
coocM= numpy.zeros((l_1,l_2))


#for bow in mm:
print 'tic'
for i in xrange(len(mm)):
#for i in xrange(20000):
    bow = mm[i]
    if not i%10000: print i
    temp_counter_1 = numpy.zeros((1,l_1))
    temp_counter_2 = numpy.zeros((1,l_2))
    for ID, count in bow:        
        if ID in IDset_1:
            index=ID2index_1[ID]
            temp_counter_1[0,index]+=count
            counter_1[0,index]+=count
        if ID in IDset_2:
            index=ID2index_2[ID]
            counter_2[0,index]+=count
            temp_counter_2[0,index]+=count
    coocM=coocM+temp_counter_1.T*temp_counter_2


wd.saveCSV(dirs,'coocM_raw',brandsl,coocM)

temp2 = wd.normalize(coocM)
temp25=numpy.log(temp2)
temp3=temp25-numpy.diag(temp25.diagonal())       
wd.saveCSV(dirs,'coocM',brandsl,temp3)
draw.main(dirs,'coocM',figName='from_cooc_log')        
    
temp2 = wd.normalize(coocM)
temp25=temp2
temp3=temp25-numpy.diag(temp25.diagonal())       
wd.saveCSV(dirs,'coocM',brandsl,temp3)
draw.main(dirs,'coocM',figName='from_cooc')     
   