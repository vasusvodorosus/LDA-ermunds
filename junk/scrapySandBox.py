import scrapy
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector


fetch('http://scrapy.org')
s = SgmlLinkExtractor()
linksV = SgmlLinkExtractor.extract_links(s,response)

[k.url for k in linksV if '/direct/view/.' in k.url]

#indent = fetch or request

# first level - all forums
# http://www.edmunds.com/forums/
hxs.select('//a[@class="title"]/@href')
    # second level from all forums
    # has uncategorized discussions and folders
    # uncategorized
    hxs.select('//a[@class="forumstitle"]')
        parseThread
    #links to model specific set
    hxs.select('//table[@class="forums-list"]').select("tr/td/a")
        #thrird level, like a model-spesific threads
        # can have multiple pages ( like Forums >Automotive News & Views >Automotive News & Views-Archives)
        hxs.select('//a[@class="forumstitle"]')
            parseThread
            
#cavearts: some threads are present in more then one plase - need to use
#a dict to make a request

#how to use a list of urls for a specialized spider:
#http://stackoverflow.com/questions/8376630/scrapy-read-list-of-urls-from-file-to-scrape

class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [l.strip() for l in open('urls.txt').readlines()]

#http://stackoverflow.com/questions/8532252/scrapy-logging-to-file-and-stdout-simultaneously-with-spider-names
http://www.google.com/search?&q=cache%3Ahttp%3A//webscraping.com
http://webscraping.com/blog/Using-Google-Cache-to-crawl-a-website/
