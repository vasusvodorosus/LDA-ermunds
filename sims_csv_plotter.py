
import matplotlib.pyplot as plt
import genSimLDAlib as gsLib
import model_play as mp

def main(dirs,CSVin="simsNtweaked",figName='heatmap'):
	
	figfname=dirs.indir+'\\'+figName+'.png'
	sims,brands= mp.loadCSV(dirs,CSVin)

	fig = plt.figure(figsize=(11,9))
	ax = fig.add_axes([.1,.1,.8,.8]) # ruined by corobar


	imgplot = ax.imshow(sims,interpolation='none')
	
	idx= xrange(len(brands))
	
	ax.set_yticks(idx)
	ax.set_yticklabels(zip(brands,idx))


	
	 
	ax.set_xticks(idx)
	ax.set_xticklabels(brands,rotation=90)
	plt.colorbar(imgplot)

	ax.set_position([.1,.2,.6,.6])
	fig.savefig(figfname)
	plt.show()



def plotSims(sims,brands,dirs,figName='heatmap'):	
    fig = plt.figure(figsize=(11,9))
    ax = fig.add_axes([.1,.1,.8,.8]) # ruined by corobar
    
    imgplot = ax.imshow(sims,interpolation='none')
    	
    idx= xrange(len(brands))
    	
    ax.set_yticks(idx)
    ax.set_yticklabels(zip(brands,idx))
    
    ax.set_xticks(idx)
    ax.set_xticklabels(brands,rotation=90)
    plt.colorbar(imgplot)
    
    ax.set_position([.1,.2,.6,.6])
    
    figfname=dirs.indir+'\\'+figName+'.png'
    fig.savefig(figfname)
    plt.show()


if __name__ == '__main__':
	dirs = gsLib.LDAdirs(indir=r"Z:\ermunds\results\sink"
						,modelName="All2passes_20topics")	
	main(dirs)