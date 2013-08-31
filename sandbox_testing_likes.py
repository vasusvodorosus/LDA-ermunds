# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:28:54 2013

@author: Vasya
"""
import ldaModel2bradsSims_direct as mp
import sims_csv_plotter
import genSimLDAlib as gsLib
import gensim

#dirs = gsLib.LDAdirs(modelName = 'PricesStemmed20passes_20topics',indir = r"Z:\ermunds\results\1 prices paid\5-6-2013")
dirs = gsLib.LDAdirs(indir=r"Z:\ermunds\results\all branded threads",    modelName="All2passes_20topics")



dict1 = gensim.corpora.dictionary.Dictionary().load(dirs.dictFileName)
lda = gensim.models.ldamodel.LdaModel(id2word=dict1).load(dirs.modelFname)

simsR, brands =  mp.corrBrands(lda)
sims = mp.normalize(simsR)
##mp.saveCSV(dirs,'simsN',brands,sims)

#sims,brands= mp.loadCSV(dirs,"simsN")
##sims_csv_plotter.main(dirs,CSVin="simsN",figName='fromTopics')


brands[brands.index('mercedes-benz')]='mercedesbenz'
mp.likes(sims,brands,brands[0])
print 'tada'

mp.likes2(lda,brands,word='luxury') # looks like sims cvs

#print debugv
#print simsR[0,:]

#print simsR[0,0]*1e5
#print mp.corrWords(lda, brands[0],brands[0])*1e5
#print (sims[0,:]*100).astype(int)
'''
toyota................100 
suzuki.................99 toyota.................99
lincoln................99 lincoln................92
subaru.................85 cadillac...............91
audi...................77 chevrolet..............88
hyundai................63 kia....................74
'''