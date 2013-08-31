import parserEdmund
from datetime import datetime

IDs =   parserEdmund.readLoadedIDs()
items = parserEdmund.PopulateFromIDList(IDs)


PagesDownloaded = sum([I.pagesLoaded for I in items])
print '\nPagesDownloaded:'+str(PagesDownloaded)

PostsDownloaded1 = sum([I.pagesLoaded*10 for I in items if I.pages > I.pagesLoaded])
PostsDownloaded2 = sum([I.Nposts for I in items if I.pages<=I.pagesLoaded])
print 'PostsDownloaded:'+str(PostsDownloaded1)+"(active threads)+"+str(PostsDownloaded2)+"(done threads)"


active = sorted([(I.pagesLoaded,I.pages,I.title,I.ID ) for I in items if I.pages-1>I.pagesLoaded])

est = sum([(-x+y)*2.0/60/60 for (x, y, z,t) in active])

print '\n(nearly)Active Threads(+-1 page):'+str(len(active))
print str(int(est))+"h estimated to finish active"
for t in active: print t

done  = sorted([(I.pagesLoaded,I.pages,I.title,I.ID) for I in items if I.pages<=I.pagesLoaded])

    
 
