# former model_play
# ldaModel2bradsSims_direct 
'''
computes distances between words from lda model using 
Dasha's metric sum(p[w1|t]*p[w2|t],t)
'''
import gensim
import someBrandFiltering as bf
import genSimLDAlib as gsLib
import numpy
import csv

def filterlines(str,fname):
    ls = []
    with open(fname,'r') as f:
        for l in f:
            if l.find(str)!=-1: ls.append(l.strip())
    for l in ls:
        print l
    return ls


def corrWords(lda, w1,w2):
    id1=lda.id2word.token2id[gsLib.wordCleanUp(w1)]
    id2=lda.id2word.token2id[gsLib.wordCleanUp(w2)]
    p=[]
    for i in xrange(lda.num_topics):
        topic = lda.state.get_lambda()[i]
        topic = topic / topic.sum()
        p.append(topic[id1]*topic[id2])
        #print i,w1,w2,'{:5.5f}'.format(p[-1]*1e6)
    return sum(p)


def corrBrands(lda,brandListFileName=r".\wordlists\brands.txt"):
    brands= [b for b in bf.getMakes(brandListFileName)if b.find(' ')==-1]
    br_tokens=[gsLib.wordCleanUp(gsLib.textCleanUp(word)) for word in brands]
    
    #try if brands are not in dict
    br_ids=[]; bad_brands=[]
    for (i,brt) in enumerate(br_tokens):    
        try:
            ID=lda.id2word.token2id[brt]
            print brands[i] ,lda.id2word.dfs[ID]
        except KeyError:
            print 'no '+ brt + ' in dict'
            bad_brands.append(brands[br_tokens.index(brt)])
    #update
    brands=sorted(list(set(brands)-set(bad_brands)))
    br_tokens=[gsLib.wordCleanUp(gsLib.textCleanUp(word)) for word in brands]
    br_ids=[lda.id2word.token2id[brt] for brt in br_tokens]        
            
    topics = lda.state.get_lambda()
    topics = [topic / topic.sum() for topic in topics]
    l=(len(brands));
    sims = numpy.zeros((l,l))
    for i in xrange(l):
        for j in xrange(l):
                p= sum([t[br_ids[i]]*t[br_ids[j]] for t in topics])
                sims[i,j]= p
                
    return (sims,brands)

def normalize(sims):
    simsN = numpy.array(sims)
    for i in xrange(len(sims)):
        n=numpy.sqrt(sims[i,i])
        simsN[i,:]=simsN[i,:]/n
        simsN[:,i]=simsN[:,i]/n
    return simsN

def likes(sims,brands,brand='acura'):
    '''
    generates likes of brand 
    '''
    ibrand = brands.index(brand)
    idx = numpy.argsort(-sims[ibrand,:])
    for i in idx:
        print "{:.<15}{:.>10,}".format(brands[i],(100*sims[ibrand,i]).astype(int))
    return idx

def likes2(lda,brands,word='acura'):
    '''
    prints likes of word -terrible in fact - should not use corr words
    because calling lda.state.get_lambda numerous times
    '''
    simvector=numpy.zeros(len(brands))
    for i,brand in enumerate(brands):
        simvector[i]= corrWords(lda, brand,word)/numpy.sqrt(corrWords(lda, brand,brand))
        
    simvector =simvector/numpy.sqrt(corrWords(lda, word,word))
    idx= numpy.argsort(-simvector)    
    for i in idx:
        print "{:.<15}{:.>10,}".format(brands[i],(100*simvector[i]).astype(int))
    return simvector


def saveCSV(dirs,CSVname,brands,sims):
    with open(dirs.indir+"\\"+CSVname+".csv", 'w') as f:
        writer = csv.writer(f)
        titles = brands
        writer.writerow(titles)
        for ib in xrange(len(brands)):
            sv = sims[ib,:]
            writer.writerow(sv)

def loadCSV(dirs,CSVname='sims'):
    fn= dirs.indir +"\\"+ CSVname+".csv"
    
    sims= numpy.loadtxt(open(fn,"rb"),delimiter=",",skiprows=1)
    with open(fn,'r') as f:
	brands = f.readline().strip().split(',')
    return (sims,brands)

def generateCSV(indir=r"Z:\ermunds\results\sink",modelName="unbranded220topics",suffix = ''):
    dirs = gsLib.LDAdirs(modelName,indir)
    dict1 = gensim.corpora.dictionary.Dictionary().load(dirs.dictFileName)
    lda = gensim.models.ldamodel.LdaModel(id2word=dict1).load(dirs.modelFname+suffix)


    simsR, brands =  corrBrands(lda)
    simsN = normalize(simsR)
    saveCSV(dirs,'simsR',brands,simsR)
    saveCSV(dirs,'simsN',brands,simsN)
    
    #mm=gensim.corpora.MmCorpus(dirs.corpusFname)
    #filterlines("topic #1:" , dirs.logFileName)
    #filterlines("ing +" , fname)
    #filterlines("at document #2000/" , fname)
    #filterlines("topic diff=" , fname)
    
    
    
if __name__ == '__main__':
    generateCSV(indir=r"Z:\ermunds\results\sink",modelName="unbranded220topics",suffix = '')