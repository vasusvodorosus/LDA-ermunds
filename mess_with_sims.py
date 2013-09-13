'''
nothing important - I was playing here to get idea about how to plot 
a similarity matrix and cluster results
'''

import numpy
import genSimLDAlib as gsLib
import ldaModel2WD as mp
import sims_csv_plotter as draw


def swap(idx,tup):
   idx[tup[0]],idx[tup[1]]=idx[tup[1]],idx[tup[0]]
   
def sort_a_slice(idx,sims,a,b,compare_to,sign=-1):
    '''
    changes the idx permutation in the way that a to b slice is sorted 
    comparing to the brand with original index compate_to
    '''
    tail = idx[a:b]
    idx2 = numpy.argsort(sign*sims[compare_to,tail])
    tail=tail[idx2]
    idx[a:b]=tail


def select(sims,brands,idx):
    '''
    reorders sims matrix and brands list accorsing to permutation idx
    '''
    newsims=numpy.zeros((len(idx),len(idx)))    
    
    for newi,oldi in enumerate(idx):		 
        for newj,oldj in enumerate(idx):
            newsims[newi,newj] = sims[oldi,oldj]
    nbrands=list()
    
    for i in range(len(idx)):
        nbrands.append(brands[idx[i]])
    return (newsims,nbrands)


def shuffle_sims(sims,brandsOld,brandsNew):
    '''
    reorders sims matrix from brandsOld to  brandsNew
    '''
    idx=numpy.zeros(len(brandsNew),dtype=int)
    for i,b in enumerate(brandsNew):
        idx[i]=brandsOld.index(b)
    (sims,nbrands)=select(sims,brandsOld,idx)
    return sims
    

# works with 20 topics on unnamend threads and WD as metric
BrandsClustered_1= list(['jeep','ram', 'gmc', 'dodge', 'maserati',    'lincoln',
                         'buick', 'cadillac', 'chevrolet','suzuki','srt', 'saab', 'mitsubishi', 'subaru', 
                         'honda', 'mazda', 'scion',  'volvo', 'acura','volkswagen','nissan','porsche','toyota','hyundai',
                         'kia',
                         'jaguar','lexus','infiniti', 'audi', 'bmw', 'tesla','fiat','chrysler', 'ford'])

# no idea...
BrandsClustered_0= list(['ram', 'gmc', 'dodge', 'jeep', 'saab', 'chrysler', 'fiat', 'lincoln',
                         'buick', 'cadillac','srt', 'maserati', 'chevrolet', 'mitsubishi', 'subaru','suzuki', 'nissan',
                         'honda', 'mazda', 'scion', 'kia','hyundai',
                         'toyota',  'volvo', 'acura','volkswagen','infiniti', 
                         'jaguar', 'porsche','mercedes-benz', 'lexus', 'audi', 'bmw', 'tesla', 'ford'])

# i think these are for the the cat-wors model
BrandsClustered_3 = ['toyota','ram', 'dodge', 'lincoln', 'gmc', 'ford', 'chevrolet','nissan', 'jeep', 
                     'suzuki', 'lexus','buick',                    
                     'kia', 'hyundai', 'fiat', 'mitsubishi', 'saab', 
                     'chrysler', 'volkswagen',   'tesla','mercedes-benz','volvo',
                     'maserati','cadillac','srt','porsche', 'audi', 'bmw','infiniti',
                     'mazda','acura', 'honda', 'scion', 'jaguar','subaru']




def main():
    '''
    resorts sims and saves a png copy
    '''
 #  dirs = gsLib.LDAdirs(indir=r"Z:\ermunds\results\all\all unbranded threads",modelName="unbranded2passes_20topics")
   #dirs = gsLib.LDAdirs(indir=r"Z:\ermunds\results\all branded threads",    modelName="All2passes_20topics")
    dirs = gsLib.LDAdirs(indir=r"Z:\ermunds\results\all unbranded threads 2",    modelName="unbranded220topics")
    #dirs = gsLib.LDAdirs(indir=r"Z:\ermunds\results\sink",    modelName="unbranded220topics")    
    
    CSVin= "simsN_posts"
    CSVout= "simsNtweaked"
    suffix=''
    figName='heatmap_from_posts_no whitening'+suffix
    #mp.generateCSV(indir=dirs.indir,modelName=dirs.modelName,suffix = suffix)
    sims,brands= mp.loadCSV(dirs,CSVin)

    nbrands= BrandsClustered_1
    # caps bug of may 14
    del nbrands[nbrands.index('mercedes-benz')]
    

    idx=numpy.zeros(len(nbrands),dtype=int)
    for i,b in enumerate(nbrands):
          idx[i]=brands.index(b)
    '''      
    ibrand = brands.index('ram')
    idx = numpy.argsort(-sims[ibrand,:])
    ibrand = brands.index('jeep')
    sort_a_slice(idx,sims,a=6,b=None,compare_to=ibrand)
    
    ibrand = brands.index('nissan')
    sort_a_slice(idx,sims,a=10,b=None,compare_to=ibrand)
    
    ibrand = brands.index('chrysler')	
    sort_a_slice(idx,sims,a=15,b=None,compare_to=ibrand)

    ibrand = brands.index('bmw')	
    sort_a_slice(idx,sims,a=23,b=None,compare_to=ibrand,sign=1)
	
    '''
    (sims,nbrands)=select(sims,brands,idx)
    mp.saveCSV(dirs,CSVout,nbrands,sims)

    draw.main(dirs,CSVout,figName)
    #1/0
	
if __name__ == '__main__':
	main()