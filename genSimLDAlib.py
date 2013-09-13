'''
utility functions to build dictianary from documens, e&
'''
import os
import logging
import gensim
import itertools
from  stemming.porter import stem

class LDAdirs(object):
    '''
    some file naming locif for projects
    this generates file names from model name
    '''
    def __init__(self,modelName = 'out40iters',indir = r'.\out'):
        self.indir=indir
        self.modelName=modelName
        self.dictFileName =os.path.join(self.indir,self.modelName+'.dict')
        self.corpusFname = os.path.join(self.indir,self.modelName+'.mm')
        self.modelFname   =os.path.join(self.indir,self.modelName+'.ldam')
        self.logFileName =os.path.join(self.indir,self.modelName+'.log.txt')
        self.dataFileName =os.path.join(self.indir,self.modelName+'.pickled.data')
        self.allDocsFileName=os.path.join(self.indir,self.modelName+'.allDocs.txt')

def getIrrDict(path=".\wordlists\irr.txt"):
    '''
    irregular verbs stemming
    '''
    irr = dict()
    with open(path, 'r') as f:
        for l in f:
            w0 = l.split()[0].lower()
            for w in l.strip().split():
                w1 = stem(w.lower())
                if w1 != w0 : irr[w1]=w0

    return irr

def textCleanUp_old(text_0):    
    '''
    old text cleanup resulting in stitching of punctuation
    '''
    return ''.join(e for e in text_0.replace('\n','') if e.isalpha() or e ==' ').lower()

def textCleanUp(text_0):
    '''
    cleans up text by removing numbers and punctuation
    handles punctuatio better -changes to spaces,as opposed to removing
    matplotlib has  taken over text bastards!!!
    '''
    
    '''
    def helper()    
        str1=''
        for i in xrange(256):
            if  chr(i) in string.letters+string.letters.upper():
                str1+=chr(i)
            else:
                    str1+=" "
        print str1.lower()
   '''
    str2='                                                                 abcdefghijklmnopqrstuvwxyz      abcdefghijklmnopqrstuvwxyz                                                                                                                                     '
    return text_0.translate(str2)

def wordCleanUp(word, irrDict=None):
    """
    stem and change verbs to present tense
    """
    w = stem(word.lower())
    try:
        return irrDict[w]
    except (TypeError, KeyError):
        return w
    

def world_list2IDs(dict1,raw_brands,tokenizef=wordCleanUp):
    ''' not sure if this is used anymore'''
    
    i=0;tokenl=[];brandsl=[];IDl=[];ID2index=dict()
    for i,b in enumerate(raw_brands):
        token =tokenizef(b);
        if len(token.split()) >1:
            raise Exception('{}:only one word brands are alowed (for now)'.format(token))
            1/0
        try:            
            ID = dict1.token2id[token]
            tokenl.append(token)
            brandsl.append(b)
            IDl.append(ID)
            ID2index[ID]=i;i=i+1
            #print "  ",b, token, ID, ": OK"
        except KeyError:
            raise Exception('brand {} tokenized to {} is not in the dictionary'.format(b,token))
            1/0
    return (brandsl,IDl,ID2index)



def swords(stopWordsFiles=None):
    '''
    list of stop words from files
    '''
    if stopWordsFiles==None:
        stopWordsFiles=[os.path.join(r'.\stoplists','stop.txt' ),os.path.join(r'.\stoplists','common.txt' )]
    sw = []
    for stopWordsFile in stopWordsFiles:
        with open(stopWordsFile) as fstop:
            for l in fstop:
                w = l.split('|')[0].lower().replace('\n','').replace(' ','').replace("'",'')
                if len(w)>1 : sw.append(w)
        return sw


def grooper(n, iterable, padvalue=None):    
    """ Yield successive n-sized chunks from iterable.
    """
    return itertools.izip(*[itertools.chain(iterable, itertools.repeat(padvalue, n-1))]*n)

def getDoc(fileName):
    """
    iterator to docs on disk
    i'm pretty sure that files are iterators. to be refactored and removed
    """
    with open(fileName, 'r') as f:
        for l in f:
            yield l


class corpusAdapter(object):
    """
    created from text, dictionary and depends on a cleanup function
    
    on iteration produces a sparse vector which can be serialized by gensim
    to be later used for LDA
    """
    def __init__(self, fname,id2word):
        self.id2word = id2word
        self.fname = fname
        self.irrDict =getIrrDict()
        
    def __iter__(self):
         for line in open(self.fname):
            words = [wordCleanUp(word, self.irrDict) for word in line.lower().split(" ")] 
            yield self.id2word.doc2bow(words)




def build_dict(dirs):
    """
    builds a dictionaary from a file dirs.allDocsFileName
    uses stopwords from file, porter stemming and irreguler verbs
    filters words <3 letters and >12
    does not filter post authors
    memory only occupied by dict
    1.5h per 1GB of text
    
    dirs is object of class LDAdirs(object)
    """ 
    logging.log(logging.INFO,"building dict")
    dict1 = gensim.corpora.dictionary.Dictionary()
    irrDict= getIrrDict()
    
    # put words into gensim dictionary by 5000
    for chunk in grooper(5000, getDoc(dirs.allDocsFileName), padvalue=""):
        # 3.74 s per loop - 
        temp=[[wordCleanUp(word, irrDict) for word in text.lower().split(" ")]for text in chunk]
        dict1.add_documents(temp)

    logging.log(logging.INFO,"initial dict:%s" % str(dict1))

    # clean ups 
    s = sorted(dict1.values(), key = len)
    stoplist = [w for w in s if len(w)<3 or len(w)>12]
    stoplist+= [wordCleanUp(w, irrDict) for w in swords()]
    logging.log(logging.INFO,"words to reject:%d" % len(stoplist))
    wset = set(s)
    stop_ids = [dict1.token2id[sw] for sw in stoplist if sw in wset]
    dict1.filter_tokens(bad_ids = stop_ids)
    dict1.filter_extremes(no_below=5, no_above=0.5, keep_n=100000)
    dict1.compactify()
   
    logging.log(logging.INFO,str(dict1))
    return dict1
    
    
def  readlineX(x,fileN):
    fp = open(fileN)
    for i, line in enumerate(fp):
        if i == x:
            return line.strip()
    fp.close()

def make_sense(i,lda,mm,docsfilename):
    '''
    just prints some infor on document number i
    '''
    topics = sorted(lda[mm[i]], key= lambda (x): x[1],reverse=True);
    print 'Text:'
    print readlineX(i,docsfilename)
    print 'KeyWords'
    print    ' '.join([lda.id2word[ID] for ID,_ in mm[i]])
    print '-------'
    for t,p in topics:
        print  '__with prob:{}% is: {}'.format(int(p*100), ' '.join([w for _,w in lda.show_topic(t,10)]))
    

def loadStuff(dirs):
    '''
    load dictionty, corpus and lda model from disc
    '''
    dict1 = gensim.corpora.dictionary.Dictionary().load(dirs.dictFileName)
    mm=gensim.corpora.MmCorpus(dirs.corpusFname)
    lda = gensim.models.ldamodel.LdaModel(id2word=dict1).load(dirs.modelFname)
    return (dict1,mm,lda)
 