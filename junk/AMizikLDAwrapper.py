import os
import parserEdmund
from subprocess import call
import subprocess
import glob
import datetime

def runMizikLDA(numTopics,path=r"C:\home\My Dropbox\dasha\ams\code"):
    cwd=os.getcwd()
    os.chdir(path)
    try:
        with open('log.txt','a') as flog:
            proc = subprocess.Popen("""lda.cmd -ldarun -rawtextfile -numtopics """ +str(numTopics),stdout=subprocess.PIPE)
            for line in iter(proc.stdout.readline,''):
                if line.find("elapsed time")==-1:
                    if line.find("log2")!=-1:
                        print line[:52] +"  "+ line[line.find("token"):].rstrip()
                    else:
                        print line.rstrip()
                flog.write(line)
                                
    except KeyboardInterrupt:
        print "...."
        

    files = filter(os.path.isfile, glob.glob("*.ldax"))
    file_date_tuple_list = [(x,os.path.getmtime(x)) for x in files]
    file_date_tuple_list.sort(key=lambda x: x[1])

    print "using the latest model file:"
    print file_date_tuple_list[-1]

    proc = subprocess.Popen("""lda.cmd -ldaexporttopics """+file_date_tuple_list[-1][0]+""" -rawtextfile""")
    proc.wait()
    print "topics exported, exporting report"
    
    proc = subprocess.Popen("""lda.cmd -ldaprint """+file_date_tuple_list[-1][0]+""" -rawtextfile >report.txt""")
    proc.wait()
    print "report exported"
    
    os.chdir(cwd)

def cleanUp(LDApath=r"C:\home\My Dropbox\dasha\ams\code",topics=True,models=True,inputs=True,report=True):
    TopicFiles = filter(os.path.isfile, glob.glob(os.path.join(LDApath,'topic',"*.*")))
    ModelFiles = filter(os.path.isfile, glob.glob(os.path.join(LDApath,"*.ldax")))
    InputFiles = filter(os.path.isfile, glob.glob(os.path.join(LDApath,'xml',"*.*")))
    ReportFiles= filter(os.path.isfile, glob.glob(os.path.join(LDApath,"report.txt")))
    ReportFiles=ReportFiles+ filter(os.path.isfile, glob.glob(os.path.join(LDApath,"log.txt")))
    all_files=[]
    if topics: all_files = all_files+ TopicFiles
    if models: all_files = all_files+ ModelFiles
    if inputs: all_files = all_files+ InputFiles
    if report: all_files = all_files+ ReportFiles
    
    tempdir = os.path.join(r"c:\temp",str(datetime.datetime.now()).replace(':','_').replace('.','_'))
    os.mkdir(tempdir)

    for f in all_files:
        head, tail = os.path.split(f)
        os.rename(f,os.path.join(tempdir,tail))
    print tempdir 

def runLDAByID(ID,numtopics=20,path='Z:\ermunds'):
    cleanUp()
    tread = parserEdmund.threadEdmundBasic()
    tread.populate(ID,path)
    comment = tread.title +" "+ tread.ID
    print comment
    parserEdmund.export2MizikInterview(tread.getPosts(),comment)
    runMizikLDA(numtopics)
    cleanUp()
    
def main():    
    IDList = parserEdmund.readLoadedIDs()
    threads = parserEdmund.PopulateFromIDList(IDList)
    x = [(tr.pagesLoaded, tr.title, tr.ID, tr) for tr in threads]
    biggest = sorted(x)[-50:]
    tr = next(tu for tu in x if tu[2]=='ef0a892')[3]
    # [(a[1], a[0], a[2]) for a in biggest if a[1].find('edan')!=-1]
    #x ('GM News, New Models and Market Share - READ ONLY', 3200, 'f16697b')
    # ('Midsize Sedans 2.0', 1805, 'f12d514'),
    # ('Midsize Sedans Comparison Thread - READ ONLY', 1230, 'ef733f6'),
    #x ('Entry Level Luxury Performance Sedans', 1603, 'ef0a892'),
    # tr = biggest[1][3]
    #  ('High End Luxury Cars', 2473, 'ee9e5eb')]
    print tr.title
    comment = tr.title +" "+ tr.ID
    parserEdmund.export2MizikInterview(tr.getPosts(),comment)
    runMizikLDA(100)
    cleanUp()

