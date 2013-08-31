# -*- coding: utf-8 -*-
"""
Created on Tue May 14 23:52:27 2013

@author: Vasya
"""
import gensim
import logging
import genSimLDAlib as gslib

#import someBrandFiltering as bf
num_topics=100
num_passes=2
dirs = gslib.LDAdirs(indir=r"Z:\ermunds\results\sink",    modelName="unbranded220topics")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filename=dirs.logFileName,
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
console.setFormatter(formatter);logging.getLogger('').addHandler(console)

logging.info("adding more from beh2.py")
dict1 = gensim.corpora.dictionary.Dictionary().load(dirs.dictFileName)
mm=gensim.corpora.MmCorpus(dirs.corpusFname)

#lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=dict1, num_topics=num_topics, update_every=0, passes=num_passes)
lda = gensim.models.ldamodel.LdaModel(id2word=dict1).load(dirs.modelFname)

for i in xrange(9):
    lda.update(mm);
    lda.save(dirs.modelFname+"_"+str(i+19));
    for t in lda.show_topics(-1):
        logging.info(str('all topics here')+t);
lda.save(dirs.modelFname+'__')