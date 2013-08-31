# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class EdmundThread(Item):
    ID = Field()
    title = Field()
    posts = Field()
    URL = Field()
    pages = Field()
    pagesLoaded = Field()
    
    
