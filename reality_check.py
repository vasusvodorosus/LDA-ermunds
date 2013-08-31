# -*- coding: utf-8 -*-
"""
Created on Fri May 17 14:31:58 2013

@author: Vasya
"""
#import gensim
import genSimLDAlib as gslib
import mess_with_sims as sims
import numpy

dirs = gslib.LDAdirs(indir=r"Z:\ermunds\results\2012 20topics",    modelName="201220topics")
docsfilename=dirs.allDocsFileName
(dict1,mm,lda)=gslib.loadStuff(dirs)

brands = sims.BrandsClustered_1

# decompose a post into topics and ptint them
gslib.make_sense(1,lda,mm,docsfilename)

# guess the topic of concept list
consepts= ['cheap','ugly','unrelaible']
consepts= ['young','trendy','fast','macho'] # fail
consepts= ['green','environment','sustainable','hybrid'] #n75
consepts= ['reliable','safe'] # n8
consepts= 'air hot heat cool exhaust system fan coolant temp blow'.split() # n5
ws,IDl,ID2index = gslib.world_list2IDs(dict1,consepts,tokenizef=gslib.wordCleanUp)
for t,p in lda[ [(t,1) for t in IDl] ]:
        print  '__with prob:{}% is N{}: {}'.format(int(p*100),t, ' '.join([w for _,w in lda.show_topic(t,10)]))
        

# rank brands withing a topic
brands = (sims.BrandsClustered_1) + ['leaf','prius','volt','camaro']
brands,IDl,ID2index = gslib.world_list2IDs(dict1,brands,tokenizef=gslib.wordCleanUp)
topicN=5
topic = lda.state.get_lambda()[topicN]
probss = sorted([(topic[ID],brands[ID2index[ID]]) for ID in IDl],reverse=True)
for p in probss: print p

## rank topics by brand/word
word = 'toyota'
_,IDl,_ = gslib.world_list2IDs(dict1,[word],tokenizef=gslib.wordCleanUp)
topics = lda.state.get_lambda()
probs = numpy.zeros(lda.num_topics)
for i,t in enumerate(topics): probs[i] =topics[i][IDl[0]]/sum(t)
idx= numpy.argsort(-probs)
for i in idx[0:5]: print i,probs[i]
lda.show_topic(idx[0])
lda.show_topic(idx[1])

#   


    