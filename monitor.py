import os
from datetime import datetime
from time import sleep

def get_size(start_path = '.'):
    total_size = 0
    total_files = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
            total_files +=1
    return (total_size,total_files)

def format_rep_str(rep):
    gb = rep[0]>>30
    mb = (rep[0] - (gb<<30))>>20
    return "|" +str(rep[1])+" pages | " + str(gb) +("GB ") + str(mb) +("MB ") +"|"+str(rep[0]) + "|"
    

repRAW =   get_size(u'Z:\ermunds\dump')
repClean = get_size(u'Z:\ermunds\data')
t= datetime.now()
while 1:
    oldrepRAW=repRAW
    repRAW =   get_size(u'Z:\ermunds\dump')
    oldrepClean=repClean
    repClean = get_size(u'Z:\ermunds\data')
    oldt = t
    t=datetime.now()
    s       = str(t) + "|"+ str(repClean[1]) +" threads "+ format_rep_str(repRAW)
    print s
    s2      = str(t-oldt) + "|+"+ str(repRAW[1]-oldrepRAW[1])+'pages|+'+str((repRAW[0]-oldrepRAW[0])>>20)+"MB"+"|"
    print s2
    with open('log', 'a') as flog:
        flog.write(s+'\n')
    sleep(3600)
    

