import parserEdmund
from collections import defaultdict

def init():
    IDList = parserEdmund.readLoadedIDs()
    threads = parserEdmund.PopulateFromIDList(IDList)
    threads = sorted(threads,key=lambda x: x.title)
    return threads

def selectTup(threads,str1):
    selection = [(a[1], a[0]) for a in enumerate(threads) if a[1].title.find(str1)!=-1]
    return selection

def select(threads,str1):
    selection = [a for a in threads if a.title.find(str1)!=-1]
    return selection

def getMakes(fname=r".\wordlists\brands.txt"):
    with open(fname) as f:
        b = [l.strip().split("|")[0] for l in f]
    return [br.lower() for br in b if len(br)>1]

def main(str1 = "Prices Paid and Buying Experience"):
      return notMain(str1)

def notMain(str1=""):
    """
    conflict resolution:
    if one thread has more han one brand it goes unter the first brand
    => no data duplication
    """
    threads   = select(init(),str1)
    brands = getMakes()+['unbranded']

    dTr = defaultdict(list)
    loneThreadCount = 0
    
    for t in threads:
        # these brands are mentioned int the thread name
        bs = [b for b in brands if t.title.lower().find(b)!=-1]
        if len(bs) >0 :
            dTr[bs[0]].append(t)
        else:
            loneThreadCount+=1
            dTr['unbranded'].append(t)
            
    print "loneThreadCount ",loneThreadCount
    counts=defaultdict(int)
    for brand in dTr: counts[brand] = sum([thread.Nposts for thread in dTr[brand]])
    for b in brands:
        print "{:.<15}{:.>10,}".format( b, counts[b])
    #for b in sorted(counts, key=counts.get, reverse=True):print b, counts[b]/1000,"K"
    return dTr 

if __name__ == '__main__':
    notMain()