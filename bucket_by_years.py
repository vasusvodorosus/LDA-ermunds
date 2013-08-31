# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:55:27 2013

@author: Vasya
"""

def main(outdir = r'z:\ermunds\results\sink\disected_by_year',
         threadChoseStr='',
         modelTag='unbranded2'):

    
    dTr = bf.notMain(threadChoseStr)
    dTr = {'unbranded':dTr['unbranded']} #!!!!!!!!!
    

    dirs =gslib.LDAdirs(modelName,outdir)
    with open(dirs.dataFileName,'a') as file1: pickle.dump(dTr,file1)

    ## setup logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        filename=dirs.logFileName,
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    console.setFormatter(formatter);logging.getLogger('').addHandler(console)


    ## get threads, extract post texts and save to single file
    # 7min per 1GB
    logging.log(logging.INFO,"building doc list")
    lineCounter=0
    with open(dirs.allDocsFileName,'a') as docDumpFile:
        for Trlist in dTr.values():
            for Tr in Trlist:
                for p in Tr.getPosts():
                    doc = gslib.textCleanUp(p.msgTitle)+gslib.textCleanUp(p.msgText)
                                        
                    lineCounter+=1
                    print(doc,file = docDumpFile)
    logging.log(logging.INFO,"total {} docs ".format(lineCounter))            

##

for 