# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 23:10:14 2013

@author: Vasya
"""
import gensim
import genSimLDAlib as gslib
import mess_with_sims
import numpy
import numpy as np
import pandas
import os

# working dir c:\python27\vasya\tutorial

def simKLdivrgence(x,y):
    return (x-y).dot(np.log(x)-np.log(y))
    

def pword_given_topic(lda):
    topics = lda.state.get_lambda()
    topics = [topic / topic.sum() for topic in topics]
    return np.array(topics)
    
def ptopic_given_word(lda,topicsPs):
    
    topics = lda.state.get_lambda()
    topics = [topic /topic.sum() * topicsPs[i] for (i,topic) in enumerate(topics)]
    topics = np.array(topics)
    return  topics/ np.sum(topics,axis = 0)


def LDA_simmetricKLdiv(probs,brands,words):
    '''
    computes fast scalar product. needs two list like objects which hold
    ID - lda word's numbers
    '''    
    lb=(len(brands));
    lw=(len(words));
    Sims = np.zeros((lb,lw))
    for ib in xrange(lb):
        for jw in xrange(lw):
            p= simKLdivrgence(probs[:,brands[ib]],probs[:,words[jw]])
            Sims[ib,jw]= p
    return Sims

def LDAscalarProd(probs,brands,words):
    '''
    computes fast scalar product. needs two dict like objects which hold
    ID - lda word's numbers
    '''
    lb=(len(brands));
    lw=(len(words));
    Sims = numpy.zeros((lb,lw))
    for ib in xrange(lb):
        for jw in xrange(lw):
                p= sum([t[brands[ib]]*t[words[jw]] for t in probs])
                Sims[ib,jw]= p
                
    return Sims
    
def LDAweights(lda,words):
    '''
    computes quare weights of words - scalar product with self
    '''
    topics = lda.state.get_lambda()
    topics = [topic / topic.sum() for topic in topics]
    l=(len(words));
    weights = numpy.zeros((l,))
    for i in xrange(l):
        p= sum([t[words[i]]**2 for t in topics])
        weights[i]= p          
    return weights
    
def pruneWordsList(words,lda):
    '''
    goes through list of words, stems them and checks if the word is in dict of LDA
    if it is, appends returns it along with count in corpus and ID in dict
    possible problem - some models were calibrated without stemming and this 
    can reject a valid word because its stem is not in dict
    '''
    words_tokens=   [gslib.wordCleanUp(gslib.textCleanUp(word)) for word in words]
    good_IDs=[];good_words=[];counts=[]
    for (i,t) in enumerate(words_tokens):    
        try:
            ID=lda.id2word.token2id[t]
            #print words[i] ,lda.id2word.dfs[ID]
            counts.append(lda.id2word.dfs[ID])
            good_IDs.append(ID)
            good_words.append(words[i])
        except KeyError:
            print 'no '+ t + ' in dict'
            
    df = pandas.DataFrame({'IDs':good_IDs,'Counts':counts},index = good_words)
    return df

def get_likes(words,brands,indir, modelName):   
    dirs = gslib.LDAdirs(modelName,indir)
    (dict1,_,lda)=gslib.loadStuff(dirs)  
    
    brands_df = pruneWordsList(brands,lda)
    words_df = pruneWordsList(words,lda)
    
    probs = pword_given_topic(lda)
    sims = LDAscalarProd(probs,brands_df["IDs"],words_df["IDs"])
    wordsWeights = LDAweights(lda,words_df["IDs"])
    brandsWeights = LDAweights(lda,brands_df["IDs"])
    sims_norm = sims/numpy.sqrt(numpy.outer(brandsWeights,wordsWeights))
    
    sims_norm_df = pandas.DataFrame(sims_norm, index=brands_df.index, columns=words_df.index)
    return(sims_norm_df,brands_df,words_df)

def get_divs(words,brands,indir, modelName,topics_marginal_probs):
     
    dirs = gslib.LDAdirs(modelName,indir)
    (dict1,_,lda)=gslib.loadStuff(dirs)  
    
    brands_df = pruneWordsList(brands,lda)
    words_df = pruneWordsList(words,lda)
    
    probs = ptopic_given_word(lda,topics_marginal_probs)
    sims = LDA_simmetricKLdiv(probs,brands_df["IDs"],words_df["IDs"])
    
    sims_norm_df = pandas.DataFrame(sims, index=brands_df.index, columns=words_df.index)
    return(sims_norm_df,brands_df,words_df)

def words_from_file(world_list_file_name):
    adjs = list()
    with open(world_list_file_name,'r') as f:
        for l in f:
            sl = l.strip();
            if len(sl.split()) ==1:
                print sl
                adjs.append(sl.split()[0])
    return adjs
    

def main(indir=r"Z:\ermunds\results\2005 20t unbranded", modelName="2005 20topics",world_list_file_name= "adjectives.txt"):
    dirs = gslib.LDAdirs(modelName,indir)
    dict1 = gensim.corpora.dictionary.Dictionary().load(dirs.dictFileName)
    lda = gensim.models.ldamodel.LdaModel(id2word=dict1).load(dirs.modelFname)

    brands = mess_with_sims.BrandsClustered_1    
    adjs= words_from_file(world_list_file_name)
    adjs.extend(brands) # just a check 
    
    
    brs = pruneWordsList(brands,lda)
    wrds = pruneWordsList(adjs,lda)
    sims = LDAscalarProd(lda,brs["IDs"],wrds["IDs"])
    wordsWeights = LDAweights(lda,wrds["IDs"])
    brandsWeights = LDAweights(lda,brs["IDs"])
    sims_norm = sims/numpy.sqrt(numpy.outer(brandsWeights,wordsWeights))
    
    sims_norm_df = pandas.DataFrame(sims_norm, index=brs.index, columns=wrds.index)
    sims_df =      pandas.DataFrame(sims, index=brs.index, columns=wrds.index)
    stats = pandas.Series([indir,modelName], index=['indir', 'modelName'])
    stats_df= pandas.DataFrame(stats)
    
    writer = pandas.ExcelWriter(os.path.join(indir,modelName+'.xlsx'))
    sims_norm_df.to_excel(writer, sheet_name='cosine distance')
    sims_df.to_excel(writer, sheet_name='raw scalar products')
    brs.to_excel(writer, sheet_name='brands')
    wrds.to_excel(writer, sheet_name='words')
    stats_df.to_excel(writer, sheet_name='stats')
    writer.save()

    
