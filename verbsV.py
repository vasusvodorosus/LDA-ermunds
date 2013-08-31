
import stemming.porter2
def getIrrDict():
    irr = dict()
    with open(".\wordlists\irr.txt", 'r') as f:
        for l in f:
            w0 = l.split()[0].lower()
            for w in l.strip().split():
                w1 = stemming.porter2.stem(w.lower())
                if w1 != w0 : irr[w1]=w0

    return irr
