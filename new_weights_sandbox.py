# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 21:22:07 2013

@author: Vasya
"""
import numpy as np
import os
import getLikes
import pandas as pd
import genSimLDAlib as gslib

modelDir = r'Z:\ermunds\results\2012 20topics'
modelName = '2012 20topics' 
topicsPs = np.genfromtxt(os.path.join(modelDir,'topics_marginal.csv'))

words = getLikes.words_from_file(r"Z:\ermunds\adjectives.txt")
brands =getLikes.words_from_file(r"Z:\ermunds\brands.txt") 


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


writer = pd.ExcelWriter(os.path.join(modelDir,modelName+'_new.xlsx'))
sims.to_excel(writer, sheet_name='cosine distance')
divs.to_excel(writer, sheet_name='KL divs')
b.to_excel(writer, sheet_name='brands')
w.to_excel(writer, sheet_name='words')
x.to_excel(writer, sheet_name='p_topic_given_word')
writer.save()

words = "Different	Distinctive	Unique	Dynamic	Innovative	Leader	Reliable	Arrogant	Authentic	Carefree	Charming	Daring	Energetic	Friendly	Fun	Glamorous	Healthy	Helpful	Independent	Intelligent	Kind	Obliging	Original	Prestigious	Progressive	Restrained	Rugged	Sensuous	Simple	Social	Straightforward	Stylish	Traditional	Trendy	Trustworthy	Unapproachable"
words=words.split()

def total_purge(words):
    cols = list()
    for year in range(2002,2013):
        print year
        modelDir = 'Z:\\ermunds\\results\\%d 20topics'%year
        modelName = '%d 20topics' %year
        dirs = gslib.LDAdirs(modelName,modelDir)
        (dict1,_,lda)=gslib.loadStuff(dirs)  
        words_df = getLikes.pruneWordsList(words,lda)
        col = words_df["Counts"]
        col.name = str(year)
        cols.append(col)
    stats = pandas.DataFrame(cols)
    return stats
    


        

        
        