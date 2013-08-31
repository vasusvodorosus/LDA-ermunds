import gensim
import logging
import parserEdmund
import pickle
import os

from genSimLDAlib import LDAdirs
"""
raw
should convert a dict Brand->Threadslist into dict Brand->LDA vectors
this was never run
needs to compute std as well
"""

def toVector(tupL,n):
    """
    converts list of (idX,value) into sparse matrix(n,1)
    """
    v = scipy.zeros((n,1))
    for (i,val) in tupL:
        #print i,v
        v[i,0]=val
    return v

def postlist2LDA(posts,ldaModel):
    """
    converts post list of into average vector in topic space
    of ldaModel
    """
    suma=toVector([],ldaModel.num_topics)
    for p in posts:
        doc = textCleanUp(p.msgTitle)+textCleanUp(p.msgText)
        doc1 = doc.lower().split()
        suma = suma+toVector(ldaModel[dict1.doc2bow(doc1)],ldaModel.num_topics)   #10ms (400tokens)
    suma=suma/len(posts)
    return suma

def postlist2LDA_Faster(posts,ldaModel):
    """
    for debug only - why so slow
    """
    n = ldaModel.num_topics
    suma=toVector([],ldaModel.num_topics)
    docs = [textCleanUp(p.msgTitle)+textCleanUp(p.msgText) for p in posts]
    gensimVecs= [ldaModel[dict1.doc2bow(text.lower().split())] for text in docs]
    vecs = [toVector(gensimVec,n) for gensimVec in gensimVecs]
    ave = sum(vecs)/len(posts)
    return ave

def Nposts(dTr):
    nposts=dict()
    for brand in dTr.keys():
        nposts[brand]=sum([len(Tr.getPosts()) for Tr in dTr[brand]])
    return nposts
              
def main(indir=r"Z:\ermunds\results\1 prices paid\20 vs 40 vs 80 iters\40",modelName="out40iters")
    dirs = LDAdirs(indir,modelName)
    
    with open(dirs.dataFileName,'r') as file1:
        dTr=pickle.read(file1)

    mm=gensim.corpora.MmCorpus(dirs.corpusFname)
    dict1 = gensim.corpora.dictionary.Dictionary().load(dirs.dictFileName)
    lda = gensim.models.ldamodel.LdaModel(id2word=dict1).load(dirs.modelFname)

    d2 = dict()
    for (k,Trlist) in dTr.items():
        topicVec = toVector([],lda.num_topics)
        counter = 0
        for Tr in Trlist:
            posts = Tr.getPosts()
            topicVec=topicVec+len(posts)*postlist2LDA_Faster(posts,lda2)
            counter+=len(posts)
        topicVec = topicVec/counter
        d2.update({k:topicVec})
        logging.log(logging.INFO,'updated:%s posts:%d',k,counter)

    np= Nposts(dTr)

    with open('d2_out','a') as file1: pickle.dump(d2,file1)
    with open('np_out','a') as file1: pickle.dump(np,file1)
