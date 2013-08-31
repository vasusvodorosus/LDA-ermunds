# -*- coding: utf-8 -*-
"""
Created on Mon Aug 05 21:12:28 2013

@author: Vasya
"""

#import gensim
import genSimLDAlib as gslib
import mess_with_sims as sims
import numpy

dirs = gslib.LDAdirs(indir=r"Z:\ermunds\results\sink",    modelName="unbranded220topics")
docsfilename=dirs.allDocsFileName
(dict1,mm,lda)=gslib.loadStuff(dirs)

brands = sims.BrandsClustered_1

# decompose a post into topics and ptint them
gslib.make_sense(1,lda,mm,docsfilename)

        
# rank brands withing a topic
brands = (sims.BrandsClustered_1) + ['leaf','prius','volt','camaro']
brands,IDl,ID2index = gslib.world_list2IDs(dict1,brands,tokenizef=gslib.wordCleanUp)
topicN=7
topic = lda.state.get_lambda()[topicN]
probss = sorted([(topic[ID],brands[ID2index[ID]]) for ID in IDl],reverse=True)
for p in probss: print p
'''
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
'''