from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
#from myproject.items import MyItem

class CombSpider(BaseSpider):
    name = 'Comb'
    allowed_domains = ['townhall-talk.edmunds.com']
    start_urls = ['http://townhall-talk.edmunds.com/WebX/.ef14c39/?127!keywords=acura&search_id=1366650770629&count=500&skip=0']

    def parseThread(self, response):
        print('inside a thread')
        hxs = HtmlXPathSelector(response)  
        filename = "xxx"+response.url.split("/")[-2][1:]
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
            yield Request(Links[0].url, callback=self.parseThread)


    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        forumThreadEntries = hxs.select('//tr[contains(@class, "discussion-item")]')
        for forumThread in forumThreadEntries:
            url = forumThread.select('td/a/@href').extract()
            #!!!
            threadID=url[0].split('/')[-1].encode('ascii','ignore')  
            threadName=forumThread.select('td/a/text()').extract()[0].encode('ascii','ignore')
            threadDate=forumThread.select('td')[1].select('text()').extract()[0].encode('ascii','ignore')
            threadTotal=forumThread.select('td')[2].select('text()').extract()[0].encode('ascii','ignore')

            print(threadName[0]+' from ' +threadDate[0] +' requesting')
            filename = "xxx"+threadID[1:]
            try:
                # if file already exists, do nothing - this might be unnessesary
                # right now it is needed because dupe reuqest is rejected afterwards,
                # in sheduler, but the file is created here and now
                with open(filename):pass
                print "been there, seen that:"+filename
            except IOError:
                with open(filename, 'a') as f:
                    f.write("threadName:"+threadName+'\n')
                    f.write("threadDate:"+threadDate+'\n')
                    f.write("threadTotal:"+threadTotal+' messages'+'\n\n')
                    f.write("threadURL:"+"http://townhall-talk.edmunds.com/direct/view/"+threadID+"/0\n\n")    
                #yield Request("http://townhall-talk.edmunds.com/direct/view/"+threadID+"/0", callback=self.parseThread)
            
# indication of a file being ready - move it to a folder?
# include navigation address, ie Forums >Sedans >Entry Level Luxury Performance Sedans
#   or just log all the pages visited to save traffic
# file operations should be moved into items pipeline  
