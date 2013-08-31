# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'tutorial'

SPIDER_MODULES = ['tutorial.spiders']
NEWSPIDER_MODULE = 'tutorial.spiders'
DOWNLOAD_DELAY = 2  
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'one time crawl for academic research'
