# -*- coding: utf-8 -*-
"""
Created on Sat Aug 03 11:59:08 2013

@author: Vasya
"""
import pandas
import getLikes
import os
import numpy as np
import genSimLDAlib as gslib


def rename_row(df,old,new):
    try:
        row = df.ix[old]
    except ValueError:
        print old, "что-то пошло не так..." 
        return df
    
    row.name = new
    df = df.drop(old)
    df = df.append(row)
    
    
    return df


def try_drop(df,c_name):
    try:
        df2 = df.drop(c_name)
    except ValueError:
        print c_name, "что-то пошло не так..." 
        return df 
    return df2
'''
# inputs:
# Natasha's file - one year per sheet
BAVfile = r"Z:\ermunds\BAV_2001_2012.xlsx"
#sheet name with data
sheet_name='2012Q4'
# model to inquire:
LDAdir=r"Z:\ermunds\results\2012 20topics"
modelName="2012 20topics"
'''

pruned_words="""Arrogant
Authentic 
Charming
Daring
Different
Distinctive
Dynamic 
Friendly
Fun
Healthy
Helpful
Independent
Innovative
Intelligent
Kind
Leader
Obliging
Original
Prestigious
Progressive
Reliable
Restrained
Rugged
Simple
Social
Stylish
Traditional
Trendy
Trustworthy
Unique""".split("\n")
pruned_words=[w.strip() for w in pruned_words ]

def load_All_BAVs(BAVfile,sheet_names):
    x = pandas.read_excel(BAVfile, sheet_names[0], index_col=0, na_values=['NA']).index
    data= dict();
    for sheet in sheet_names:
        df= pandas.read_excel(BAVfile, sheet, index_col=0, na_values=['NA'])
        x = intersect(x, df.index)
        
    for sheet in sheet_names:
        df =pandas.read_excel(BAVfile, sheet, index_col=0, na_values=['NA'])        
        good_cols = [col for col in df.columns if len(col.split("_"))==2]
        df= df[good_cols]
        df.columns = map(lambda x: x.split("_")[0],df.columns)
        
        try:        
            del df[u"Tough"]
        except:
            print "oh well"
        try:        
            del df[u"Visionary"]
        except:
            print "oh well"
        df=df[pruned_words]
        df = df.ix[x]        
        data[sheet]=df

    return (x,data)


def beh():
    BAVfile = r"Z:\ermunds\BAV_2001_2012.xlsx"
    sheet_names = [str(x)+"Q4" for x in range(2001,2013)]
    (x,data)=load_All_BAVs(BAVfile,sheet_names)
    pl = pandas.Panel(data)
    (pl['2005Q4']-pl['2004Q4']).to_excel('2005Q4-2004Q4.xlsx')
    pl.to_excel(r'Z:\ermunds\cleaned_adjs.xlsx')    
    
    
    writer = pandas.ExcelWriter('deriv_pruned.xlsx')    
    for year1, year2 in zip(pl.items[1:],pl.items[:-1]):
        diff = pl[year2]-pl[year1]
        diff.to_excel(writer, sheet_name= year1+"-"+year2)
    writer.save()
     
def main2():
    BAVfile = r"Z:\ermunds\BAV_2001_2012.xlsx"

    good_brands =intersect_brands(BAVfile,sheet_names)
    good_brands.remove(u'General Motors (GM)')
    #good_brands.remove(u'Mitsubishi Vehicles')
    #good_brands.remove(u'Mercedes-Benz')
    
    return good_brands


def intersect(s1,s2):
    return [x for x in s1 if x in s2]
    
# ----------------------------------------------------------------------------
def main(BAVfile,sheet_name,LDAdir,modelName):
    BAV_raw= pandas.read_excel(BAVfile, sheet_name, index_col=0, na_values=['NA'])
    #Hack!!! Total_Prefer_pct is th last useless col
    #idx_first = BAV_raw.columns.get_loc('Brand_Asset_C')+1
    idx_first = 1
    good_cols = [col for col in BAV_raw.columns[idx_first:] if len(col.split("_"))==2 and col.endswith('pct')]
    
    BAV_filtered = BAV_raw[good_cols]
    BAV_filtered.columns = map(lambda x: x.split("_")[0],BAV_filtered.columns)
    
    # filter brands - depends onf the dictionay creation way
    # ie if '-' goes to space this will work
    # if '-' is dropped tnen will not
    
    BAV_filtered = try_drop(BAV_filtered,'General Motors (GM)')
    BAV_filtered = try_drop(BAV_filtered,'Ford Motor Company')
    BAV_filtered = try_drop(BAV_filtered,'Smart (car)')
    BAV_filtered = try_drop(BAV_filtered,'Mini Cooper')
    
    
    BAV_filtered= rename_row(BAV_filtered,'Mercedes-Benz','Mercedes')
    BAV_filtered = rename_row(BAV_filtered,'Mitsubishi Vehicles','Mitsubishi')
    BAV_filtered = rename_row(BAV_filtered,'Rolls-Royce','Royce')
    BAV_filtered = rename_row(BAV_filtered,'Aston Martin','Aston')
    BAV_filtered = rename_row(BAV_filtered,'Alfa Romeo','Romeo')
    
    
    
    words=  [w.encode() for w in BAV_filtered.columns]
    brands= [b.encode() for b in BAV_filtered.index]
    
    topicsPs = np.genfromtxt(os.path.join(LDAdir,'topics_marginal.csv'))
    (LDA_df,BrandsInfo,WordsInfo) = getLikes.get_likes(words=words,brands=brands,indir=LDAdir, modelName=modelName)
    (divs,_,_) = getLikes.get_divs (words,brands,indir=LDAdir, modelName=modelName ,topics_marginal_probs=topicsPs)
    
    
    BAV_filtered = BAV_filtered[LDA_df.columns]
    BAV_filtered = BAV_filtered.ix[LDA_df.index]
    
    dirs = gslib.LDAdirs(modelName,LDAdir)
    (dict1,_,lda)=gslib.loadStuff(dirs)  
    probs = getLikes.ptopic_given_word(lda,topicsPs)
    probs_df =  pandas.DataFrame(probs, columns=lda.id2word.values())
    alls = pandas.concat([ BrandsInfo["IDs"] ,WordsInfo["IDs"]])
    x = probs_df[alls]
    x.columns = alls.index
    
    writer = pandas.ExcelWriter(os.path.join(LDAdir,modelName+'_BAV_comp.xlsx'))
    LDA_df.to_excel(writer, sheet_name='cosine distance')
    BAV_filtered.to_excel(writer, sheet_name='BAV')
    divs.to_excel(writer, sheet_name='KL divs') 
    BrandsInfo.to_excel(writer, sheet_name='brands')
    WordsInfo.to_excel(writer, sheet_name='words')
    
    x.to_excel(writer, sheet_name='p_topic_given_word')
    writer.save
    return (LDA_df,BAV_filtered,divs,BrandsInfo,WordsInfo)

if __name__ == '__main__':
	main()
