import parserEdmund
from datetime import datetime

t= datetime.now()
IDList = parserEdmund.readLoadedIDs()
stuff = parserEdmund.PopulateFromIDList(IDList)
print datetime.now()-t

t= datetime.now()
yearCount = dict()
for Ethread in stuff:
    for post in Ethread.getPosts():
        try:
            yearCount[post.msgTime.tm_year] +=1
        except KeyError:
            yearCount[post.msgTime.tm_year] =1
print yearCount
print datetime.now()-t
