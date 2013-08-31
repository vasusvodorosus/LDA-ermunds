import parserEdmund


IDListL = parserEdmund.readLoadedIDs()
print "total ID loaded  : %d" % len(IDListL)
IDListTotal = parserEdmund.IDListFromURLsFile(fileName='ALLurls.txt')
print "total IDs        : %d" %len(IDListTotal)
NotYetLoaded = list( set(IDListTotal)-set(IDListL))
print "not yetloaded IDs: %d" %len(NotYetLoaded)


shortIDs = [ID for ID in NotYetLoaded if len(ID)==len('f152c48')]
longIDs = list(set(NotYetLoaded)-set(shortIDs))
print "not yetloaded IDs short : %d" %len(shortIDs)
print "not yetloaded IDs long  : %d" %len(longIDs)

with open('shortIDsToDownload.txt','w') as IDfile:
    for ID in shortIDs:
            IDfile.write(ID+'\n')

with open('longIDsToDownload.txt','w') as IDfile:
    for ID in longIDs:
            IDfile.write(ID+'\n')

