from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from tutorial.items import TutorialItem

# unused
class PostsSpider(CrawlSpider):
    name = "posts"
    allowed_domains = ["townhall-talk.edmunds.com"]
    start_urls = ["http://townhall-talk.edmunds.com/direct/view/.ef21923/0"]
    rules = [Rule(SgmlLinkExtractor(restrict_xpaths=['//li[contains(@class, "next")]']), 'parseV',follow =False)]


    
    
    def parseV(self, response):
        print('-----------------Hi, this is an item page! %s' % response.url)
        print('=================')
        
        
        hxs = HtmlXPathSelector(response)
        ##entries = hxs.select('//span[contains(@id, "text_msg")]/text()').extract()
        entries = hxs.select('//span[contains(@id, "text_msg")]')
        
        for rec in entries:
            item = TutorialItem()
            a=rec.select('text()').extract()
            item['title'] = u''.join(a).encode('ascii','ignore')
            item['link'] = 1
            item['desc'] = rec.extract() 
            print "    "+item['title']
            yield item   
            
            
        
            
       
 
    
