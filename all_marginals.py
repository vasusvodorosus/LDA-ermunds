# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 23:10:26 2013

@author: Vasya
"""

brands ='''Acura
Audi
BMW
Buick
Cadillac
Chevrolet
Chrysler
Dodge
Fiat
Ford
Honda
Hyundai
Infiniti
Jaguar
Kia
Lexus
Lincoln
Mazda
Mercedes
Mitsubishi
Nissan
SAAB
Subaru
Toyota
Volkswagen
Volvo
'''.split("\n")

words = 'Arrogant	Authentic	Charming	Daring	Different	Distinctive	Dynamic	Friendly	Fun	Healthy	Helpful	Independent	Innovative	Intelligent	Kind	Leader	Obliging	Original	Prestigious	Progressive	Reliable	Restrained	Rugged	Simple	Social	Stylish	Traditional	Trendy	Trustworthy	Unique'.split()

import numpy as np
import os
import getLikes
import pandas as pd
import genSimLDAlib as gslib
import marginal_topics_distr as marginal

for year in range(2002,2013):
    print year
    modelDir = 'Z:\\ermunds\\results\\%d 20topics'%year
    modelName = '%d 20topics' %year
    
    marginal.compute_and_save(modelName=modelName, LDAdir=modelDir)
    topicsPs = np.genfromtxt(os.path.join(modelDir,'topics_marginal.csv'))
    
    (divs,_,_) = getLikes.get_divs (words,brands,indir=modelDir, modelName=modelName ,topics_marginal_probs=topicsPs)
    (sims,b,w) = getLikes.get_likes(words,brands,indir=modelDir, modelName=modelName )
    
    dirs = gslib.LDAdirs(modelName,modelDir)
    (dict1,_,lda)=gslib.loadStuff(dirs)  
    
    brands_df = getLikes.pruneWordsList(brands,lda)
    words_df = getLikes.pruneWordsList(words,lda)
    
    probs = getLikes.ptopic_given_word(lda,topicsPs)
    probs_df =  pd.DataFrame(probs, columns=lda.id2word.values())
    alls = pd.concat([ brands_df["IDs"] ,words_df["IDs"]])
    x = probs_df[alls]
    x.columns = alls.index
       
    writer = pd.ExcelWriter(os.path.join(modelDir,modelName+'_all_Aug18.xlsx'))
    sims.to_excel(writer, sheet_name='cosine distance')
    divs.to_excel(writer, sheet_name='KL divs')
    b.to_excel(writer, sheet_name='brands')
    w.to_excel(writer, sheet_name='words')
    x.to_excel(writer, sheet_name='p_topic_given_word')
    
    writer.save()