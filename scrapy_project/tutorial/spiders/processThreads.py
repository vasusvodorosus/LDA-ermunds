from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import os

# some changes are untested
# ie moving all the paths outsid code, here:
googc='http://www.google.com/search?&q=cache%3A'
googc=''
edmbase = r'http://townhall-talk.edmunds.com/direct/view/.'
databasePath = 'Z:\ermunds'
urlsFileName = r'.\IDs and URLs\shortIDsToDownload.txt'

class ProcessTreads(BaseSpider):
    name = 'processtreads'
    allowed_domains = ['townhall-talk.edmunds.com','webcache.googleusercontent.com','google.com']
    try:
        start_IDs =  [l.strip() for l in open(urlsFileName).readlines()] 
        start_urls = [edmbase+ID+"/0" for ID in start_IDs]
    except IOError:
        print "did not find urls file"

    def parse(self, response):
        print('inside a thread')
        hxs = HtmlXPathSelector(response)  
        filename_ =    response.url.split("/")[-2][1:]
        filename=      os.path.abspath(databasePath+ "\data\%s" % filename_)
        dumpFilePath = os.path.abspath(databasePath+ "\dump\%s" % filename_)
        try:
            a = response.meta['page']
        except KeyError:
            a=0
            os.mkdir(dumpFilePath)
            with open(filename, 'a') as f:
                #header
                forumTitle=hxs.select('//div[@class="module forums"]/h2/text()').extract()[0].encode('ascii','ignore').replace('\n','')
                extraInfo=hxs.select('//div[@class="module forums discussion tid"]/h4/text()').extract()[0].encode('ascii','ignore').replace('\n','')
                f.write("title:"+forumTitle+"\n")
                f.write("extraInfo:"+extraInfo+"\n")
                f.write(response.url+"\n")
                f.write(filename+"\n")
                f.write(dumpFilePath+"\n\n")
                
        with open(dumpFilePath+ "\\" +str(a)+'.html', 'a') as fd:
            fd.write(response.body)
            
        with open(filename, 'a') as f:
            for entry in hxs.select('//div[contains(@class,"forums-thread")]'):
                msgID=     entry.select('span/@id').extract()[0]        
                msgDate=   entry.select('h4/text()').extract()[0].encode('ascii','ignore').replace('\n','')
                msgText=' '.join(entry.select('span/text()').extract()).encode('ascii','ignore').replace('\n','')
                try:
                    mgAuthor=  entry.select('h3/span/a/text()').extract()[0].encode('ascii','ignore').replace('\n','')
                except:
                    mgAuthor='none'
                try:
                    msgTitle=  entry.select('h3/strong/text()').extract()[0].encode('ascii','ignore').replace('\n','')                
                except:
                    msgTitle="none"
                f.write('msgID:'+msgID+'\n')
                f.write('msgTitle:'+msgTitle+'\n')
                f.write('mgAuthor:'+mgAuthor+'\n')
                f.write('msgDate:'+msgDate+'\n')
                f.write('msgText:'+msgText+'\n\n')
        s = SgmlLinkExtractor(restrict_xpaths=['//li[contains(@class, "next")]'])
        Links = s.extract_links(response)
        if len(Links) > 0:
            print 'going to the next page'
            r = Request(googc+Links[0].url, callback=self.parse)
            r.meta['page']=a+1;
            yield r
