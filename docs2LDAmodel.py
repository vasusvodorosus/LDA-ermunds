"""
calls someBrandFiltering to get dict of
    Brand ->list of threads associated
then computes dict
flters dit using stop list from files
should save the postlist to out folder for control?
builds corpus
runs LDA

saves corpus, lda model and dict ans alldocs

"""
from __future__ import print_function
import gensim
import logging
import pickle
import time

import genSimLDAlib as gslib
import someBrandFiltering as bf


def main(outdir = r'Z:\ermunds\results\2005 20t unbranded',
         num_passes=2,
         num_topics=20,
         threadChoseStr='',
         modelTag='2005+',
         time_low_cutoff=time.strptime("1 Jan 2005", "%d %b %Y"),
         time_hi_cutoff=time.strptime("1 Jan 2006", "%d %b %Y")
         ):
    # posts are chosen between these two dates             

    
    dTr = bf.notMain(threadChoseStr)
    #dTr = {'unbranded':dTr['unbranded']} #!!!!!!!!!
    
    modelName = modelTag+str(num_topics)+'topics'
    dirs =gslib.LDAdirs(modelName,outdir)
    with open(dirs.dataFileName,'a') as file1: pickle.dump(dTr,file1)

    ## setup logging
    '''    
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        filename=dirs.logFileName,
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    console.setFormatter(formatter);logging.getLogger('').addHandler(console)
    '''
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(dirs.logFileName)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)


    ## get threads, extract post texts and save to single file
    # 7min per 1GB
    logging.log(logging.INFO,"building doc list")
    lineCounter=0
    with open(dirs.allDocsFileName,'a') as docDumpFile:
        for Trlist in dTr.values():
            for Tr in Trlist:
                for p in Tr.getPosts():
                    if (p.msgTime>time_low_cutoff) and (p.msgTime<time_hi_cutoff):
                        doc = gslib.textCleanUp(p.msgTitle)+gslib.textCleanUp(p.msgText)
                        lineCounter+=1
                        print(doc,file = docDumpFile)
    logging.log(logging.INFO,"total {} docs ".format(lineCounter))            

    #build dict 1.5H/GB
    dict1 = gslib.build_dict(dirs)
    dict1.save(dirs.dictFileName)
    #dict1 = gensim.corpora.dictionary.Dictionary().load(dirs.dictFileName)

    #pipe docfile to gensim corpus
    #fixme - corpusAdapter missing a len() property
    corpus = gslib.corpusAdapter(dirs.allDocsFileName,id2word=dict1)
    gensim.corpora.MmCorpus.serialize(fname=dirs.corpusFname, corpus=corpus, id2word=dict1)
    mm=gensim.corpora.MmCorpus(dirs.corpusFname)

    ## run the LDA (2h per update on 2M posts)
    lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=dict1, num_topics=num_topics, update_every=0, passes=num_passes)
    lda.save(dirs.modelFname+"_0")
    
    for i in xrange(9):
        lda.update(mm);
        lda.save(dirs.modelFname+"_"+str(i+1));
        for t in lda.show_topics(-1):
            logging.info(str('all topics here')+t);
    lda.save(dirs.modelFname)
    
    logger.removeHandler(ch)
    logger.removeHandler(fh)
    return modelName

if __name__ == '__main__':
	main()