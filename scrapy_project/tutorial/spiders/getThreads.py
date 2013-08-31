from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

#bug: extra links get through (ones with '/' at the end)

class AllThreads(BaseSpider):
    name = 'getAllThreads'
    allowed_domains = ['townhall-talk.edmunds.com']
    start_urls = ['http://www.edmunds.com/forums/']

    def parse(self, response):
        # title page
        hxs = HtmlXPathSelector(response)
        s1 = SgmlLinkExtractor(restrict_xpaths=['//a[@class="title"]'])
        Links = s1.extract_links(response)       
        for l in Links:
            yield Request(l.url, callback=self.parseL2)
            
    def parseL2(self, response):
        # forums - liks to lists and to threads
        s2 = SgmlLinkExtractor(restrict_xpaths=['//table[@class="forums-list"]/tr/td/a'])
        Links = s2.extract_links(response)
        for l in Links:
            yield Request(l.url, callback=self.parseL3)
        self.scrapeTheadURL(response)    
    
    def parseL3(self, response):
        # like model specific
        self.scrapeTheadURL(response)
        
        # multipage
        s = SgmlLinkExtractor(restrict_xpaths=['//li[contains(@class, "next")]'])
        Links = s.extract_links(response)
        if len(Links) > 0:
            yield Request(Links[0].url, callback=self.parseL3)

    def scrapeTheadURL(self, response):
        s3=SgmlLinkExtractor(restrict_xpaths=['//a[@class="forumstitle"]'])    
        Links = s3.extract_links(response)
        for l in Links:
            self.logLink(l)
    
    def logLink(self,l):
        print(l.url)

    
