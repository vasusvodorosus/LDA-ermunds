from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from tutorial.items import TutorialItem

class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://townhall-talk.edmunds.com/WebX/.ef14c39/?127!keywords=acura&search_id=1366650770629&count=500&skip=0"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
        
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//tr')
        items = []
        for site in sites:
            item = TutorialItem()
            item['title'] = site.select('td/a/text()').extract()
            item['link'] = site.select('td/a/@href').extract()
            item['desc'] = site.select('text()').extract()
            print item['title']
            print item['link']
            items.append(item)
        return items
       
        
            

##scrapy shell http://townhall-talk.edmunds.com/WebX/.ef14c39/?127!keywords=acura&search_id=1366650770629&count=500&skip=0
   
