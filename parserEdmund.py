import os
import time
import math

class threadEdmundBasic:
    LINES_PER_RECORD=6
    def __init__(self):
        self.ID =''
        self.title =''
        self.Nposts  =-2
        self.URL  =''
        self.pages =-1
        self.pagesLoaded =-1
        self.dataFile = ''
        
    def populate(self,ID,path):
        """
        reads thread data from ID dat file in path\data
        does not read individual posts
        """
        self.dataFile=path+'\data\\'+ID
        with open(self.dataFile,'r') as f:
            head=[f.next() for x in xrange(5)]
        self.ID= ID
        self.title= head[0].strip()[6:]
        try:
            self.Nposts= int(head[1].split('messages')[0].split('extraInfo:')[1].replace(' ',''))
        except ValueError:
            self.Nposts = -1

        self.URL= head[2].strip()
        self.pages= int(math.ceil(self.Nposts/10.0))
        self.pagesLoaded=len((os.listdir(path+'\dump\\'+ID)))

    def getPosts(self):
        """
        returns the list of posts(class post Edmund) for the thread
        """
        with open(self.dataFile,'r') as f:
            head=[f.next() for x in xrange(5)]
            contents = [line.strip() for line in f][:-1]
        records=[contents[x:x+self.LINES_PER_RECORD] for x in xrange(0, len(contents), self.LINES_PER_RECORD)]
        posts=[]
        for r in records:
            post = postEdmunds()
            post.populate(r)
            post.threadID=self.ID
            posts.append(post)
        return posts

    def __repr__(self):
        str1=[]
        str1.append('threadID:%s' % self.ID)
        str1.append('Nposts:%d' % self.Nposts)
        str1.append('title:%s' % self.title[:20] + '...')
        return '\n'.join(str1)

class postEdmunds:
    def __init__(self):
        self.threadID =''
        self.msgID =''
        self.msgAuthor=''
        self.msgTitle=''
        self.msgText=''
        self.msgTime=None
        
    def populate(self,record):
        """
        read post data from text lines in rec
        this basically defines the format of how data is stored in data file
        """
        self.msgID =record[1][6:]
        self.msgTitle=record[2][9:]
        self.msgAuthor=record[3][9:]
        self.msgText=record[5][8:]
        str1 = record[4][8:]
        try:
            self.msgTime= time.strptime(str1[:str1.find(')')+1],'%b %d, %Y (%I:%M %p)')
        except ValueError:
            self.msgTime= time.strptime("1 Jan 1900", "%d %b %Y")

    def __repr__(self):
        str1=[]
        str1.append('\nthreadID:%s' % self.threadID)
        str1.append('msgID:%s' % self.msgID)
        str1.append(time.strftime("%d %b %Y %H:%M", self.msgTime))
        str1.append('msgAuthor:%s' % self.msgAuthor)
        str1.append('msgTitle:%s' % self.msgTitle)       
        str1.append('msgText:%s' % self.msgText[:20] + '...\n')
        return '\n'.join(str1)
    
              

def readLoadedIDs(path = 'Z:\ermunds'):
    """
    reads IDs of threads stored in path\data
    returns list of ID string
    """
    LoadedIDs=[]
    for dirpath, dirnames, filenames in os.walk(path+'\data\\'):
        for f in filenames:
            if f.find(".")==-1:
                LoadedIDs.append(f)            
    return LoadedIDs


def IDListFromURLsFile(fileName='urls.txt'):
    """
    reads a list off IDs from a file containing URLs to
    threads. URLs should not have trailing page number
    good:
    http://townhall-talk.edmunds.com/direct/view/.f194582
    
    bad:
    http://townhall-talk.edmunds.com/direct/view/.f194582/341
    """
    start_urls = [l.strip() for l in open(fileName).readlines()]
    start_urls = [l for l in start_urls if l[-1]!='/']
    IDs = [l.split("/")[-1][1:] for l in start_urls]
    return IDs

def PopulateFromIDList(threadIDs,path='Z:\ermunds'):
    """
    returns a list of threadEdmundBasic objects with IDs from threadIDs
    loaded form path\data
    """
    itemList=[]
    for ID in threadIDs:
        item = threadEdmundBasic()
        item.populate(ID,path)
        itemList.append(item)
    return itemList
        
        
def export2MizikInterview(postsList,comment="",fileName=r"C:\home\My Dropbox\dasha\ams\code\xml\out.txt"):
    """
    exports text from list of topics into a txtfile
    Andrey's LDA code can analyze
    """
    with open(fileName,'w') as f:
        f.write('INTERVIEW WITH Autonatically generated Edmunds Post List matching AMS interview:'+comment+'\n\n')
        for post in postsList:
            tit = ''.join(e for e in post.msgTitle.replace('\n','') if e.isalnum() or e ==' ')
            tex = ''.join(e for e in post.msgText.replace('\n','') if e.isalnum() or e ==' ')
            f.write('TITLE '+tit.upper()+'\n\n')
            f.write('pust '+tex+'\n\n')
        f.write('End of interview\n\n')
    return 1




