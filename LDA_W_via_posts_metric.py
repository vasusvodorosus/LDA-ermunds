# -*- coding: utf-8 -*-
"""
Created on Fri May 17 08:37:21 2013

@author: Vasya
"""

import gensim
import logging
import pickle
import os
import numpy
import scipy

import genSimLDAlib as gslib
#import someBrandFiltering as bf
import sims_csv_plotter as simplot
import ldaModel2WD as mp
import mess_with_sims as sims

def generateOverlap(corpus,brandsIDset):
    docnum=0;
    docNum2IDset=dict()

    for doc in corpus:
        docIDs=set([d[0] for d in doc])
        sset = set.intersection(docIDs,brandsIDset)
        if len(sset)>0:
           docNum2IDset[docnum]=sset
        docnum=docnum+1
        if not docnum%50000: print docnum
    return docNum2IDset
                                       
def toVector(tupL,n,v):
    """
    converts list of (idX,value) into sparse matrix(n,1)
    """
    v = numpy.zeros(n)
    for (i,val) in tupL:
        #print i,v
        v[i]=val
    return v

dirs = gslib.LDAdirs(indir=r"Z:\ermunds\results\all unbranded threads 2",    modelName="unbranded220topics")
dirs = gslib.LDAdirs(indir=r"Z:\ermunds\results\sink",    modelName="unbranded220topics")


mm=gensim.corpora.MmCorpus(dirs.corpusFname)
dict1 = gensim.corpora.dictionary.Dictionary().load(dirs.dictFileName)
lda = gensim.models.ldamodel.LdaModel(id2word=dict1).load(dirs.modelFname)

raw_brands= list(['ram', 'gmc', 'dodge', 'jeep', 'saab', 'chrysler', 'fiat', 'lincoln',
                 'buick', 'cadillac','srt', 'maserati', 'chevrolet', 'mitsubishi', 'subaru','suzuki', 'nissan',
                 'honda', 'mazda', 'scion', 'kia','hyundai',
                 'toyota',  'volvo', 'acura','volkswagen','infiniti', 
                 'jaguar', 'porsche','mercedes', 'lexus', 'audi', 'bmw', 'tesla', 'ford'])


brandsl,IDl,ID2index = gslib.world_list2IDs(dict1,raw_brands,tokenizef=gslib.wordCleanUp)
brandsIDset=set(IDl)



FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(format=FORMAT)

## generate dict: docID->set of brands mentioned
docNum2IDset=generateOverlap(mm,brandsIDset)

pickle.dump(docNum2IDset, open(dirs.indir+'\\'+'docNum2IDset.pickle','w'))
#docNum2IDset=pickle.load(open(dirs.indir+'\\'+'docNum2IDset.pickle','r'))

## generate lda vectors from the posts which mention some brands

LDA_vectorsWithCooc=numpy.zeros((len(IDl),lda.num_topics))
LDA_vectorsWithOutCooc=numpy.zeros((len(IDl),lda.num_topics))

i=0;tot=len(docNum2IDset.keys())
v=numpy.zeros(lda.num_topics)
for (doc_num,doc) in enumerate(mm):
    i=i+1
    if not i%5000: 
        print '{} of {}'.format(i, tot)
        logging.info('{} of {}'.formast(i, tot))
    if docNum2IDset.has_key(doc_num):     
        LDA_vector=toVector(lda[doc],lda.num_topics,v)       
        brandIDset=docNum2IDset[doc_num]
        for brandID in brandIDset:
            LDA_vectorsWithCooc[ID2index[brandID],:]+=LDA_vector
        if len(brandIDset)==1:
            LDA_vectorsWithOutCooc[ID2index[brandID],:]+=LDA_vector

pickle.dump(LDA_vectorsWithCooc, open(dirs.indir+'\\'+'LDA_vectorsWithCooc.pickle','w'))
LDA_vectorsWithCooc=pickle.load( open(dirs.indir+'\\'+'LDA_vectorsWithCooc.pickle','r'))

pickle.dump(LDA_vectorsWithOutCooc, open(dirs.indir+'\\'+'LDA_vectorsWithOutCooc.pickle','w'))
LDA_vectorsWithOutCooc=pickle.load( open(dirs.indir+'\\'+'LDA_vectorsWithOutCooc.pickle','r'))

pickle.dump(brandsl, open(dirs.indir+'\\'+'brandsl.pickle','w'))
brandsl=pickle.load( open(dirs.indir+'\\'+'brandsl.pickle','r'))

## convert these vectors to sims 
vectors = LDA_vectorsWithCooc
#vectors = LDA_vectorsWithOutCooc

simCos=numpy.zeros((len(brandsl),len(brandsl)))

for b1i in xrange(len(brandsl)):
    for b2i in xrange(len(brandsl)):
        v1 =vectors[b1i,:]# (vectors[b1i,:] -ave)/stds
        v2 =vectors[b2i,:]# (vectors[b2i,:] -ave)/stds
        simCos[b1i,b2i] = (v1.dot(v2))/(scipy.linalg.norm(v1)*scipy.linalg.norm(v2))


mp.saveCSV(dirs,'simsN_posts',brandsl,simCos)
brandsOrdered=sims.BrandsClustered_1
simCos=sims.shuffle_sims(simCos,brandsl,brandsOrdered)

simplot.plotSims(simCos,brandsOrdered,dirs,figName='from topics '+'withRepeadedPosts')

##
for i in xrange(len(LDA_vectorsWithCooc)):
    LDA_vectorsWithCooc[i,:]=LDA_vectorsWithCooc[i,:]/sum(LDA_vectorsWithCooc[i,:])
    LDA_vectorsWithOutCooc[i,:]=LDA_vectorsWithOutCooc[i,:]/sum(LDA_vectorsWithOutCooc[i,:])


