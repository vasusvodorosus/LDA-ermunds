# -*- coding: utf-8 -*-
"""
Created on Sun May 12 17:09:36 2013
just cheking on aothors numbers ets, sandbox
@author: Vasya
"""

import gensim

import collections
import genSimLDAlib as gslib
import someBrandFiltering as bf


allthreads =bf.init()

somethreads=allthreads[0:100]

authPostCount = collections.defaultdict(int)
for t in allthreads: 
    for post in t.getPosts():
        author = post.msgAuthor
        authPostCount[author]+=1
len(authPostCount) #375,569 

authorStems=set()
for author in authPostCount.keys():
    authorStem=gslib.wordCleanUp(gslib.textCleanUp(author))
    authorStems.add(authorStem)
len(authorStems) #27,3418

for author in sorted(authPostCount.keys()):
    if author.find(' ')!=-1:
        print author


with open('authList.txt','w') as authListF:
    for author in sorted(authPostCount.keys()):
        authListF.write(author+'\n')

with open('authStemsList.txt','w') as authListF:
    for author in sorted(authorStems):
        authListF.write(author+'\n')

revlist = zip(authPostCount.values(),authPostCount.keys())
with open('authCount.txt','w') as authListF:
    for t in sorted(revlist,reverse=True):
        authListF.write(t[1]+" "+str(t[0])+'\n')

len([c for c in authPostCount.values() if c> 5]) #53,068



s = r"Z:\ermunds\results\1 prices paid\5-6-2013\PricesStemmed20passes_20topics.dict"
dict1 = gensim.corpora.dictionary.Dictionary().load(s)

tupl = []
for ID in dict1.keys():
     tupl.append((dict1.dfs[ID],dict1[ID]))   
tupl=sorted(tupl,reverse=True)

with open('wordCounts','w') as f:
    for t in tupl:
        f.write(str(t)+'\n')
        
lst= []
for b in bf.getMakes():
    token = gslib.wordCleanUp(gslib.textCleanUp(b))
    try:    
        ID=dict1.token2id[token]
        fr=dict1.dfs[ID]
        print b,fr,token
        lst.append((fr,b))
    except KeyError:
        print b,'fail',token
        
lst = sorted(lst)
fname = 'brand_mentions_count.txt'
with open(fname,'w') as outfile:
    for t in lst:
        outfile.write(t[1]+":"+str(t[0])+'\n')
        