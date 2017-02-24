
# coding: utf-8

# In[4]:

import requests
import urllib
from scrapy.http import TextResponse
from scrapy.spiders import Spider
from scrapy.selector import Selector
import pandas as pd

CATEGORIES = ["OVERALL", "STANDARD", "DISCIPLINE", "CONTROL"]
CATEGORY = "CONTROL"
PAGES = 2
        
url = "http://www.foxsports.com/soccer/stats?competition=1&season=20160&category=" + CATEGORY +"&pos=0&team=0&isOpp=0&sort=3&sortOrder=0&page="
pageData = dict()
for i in range(1,PAGES):
    currenturl = url + str(i)
    r = requests.get(currenturl)
    response = TextResponse(r.url, body=r.text, encoding='utf-8')
    pageData[currenturl] = response    


# In[11]:

gameData = pd.DataFrame()

class EPLSpider(Spider):
    name = 'ManSpider'
    allowed_domains = ["foxsports.com"]

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
    def parsePlayerStats(self, response):
        hxs = Selector(response)
        items = hxs.xpath('//table')
        my_item = dict()
        for item in items:
            playernames = item.xpath('//a[@class="wisbb_fullPlayer"]//span/text()').extract()
            team = item.xpath('//span[@class="wisbb_tableAbbrevLink"]//a/text()').extract()
            title="Total Touches"
            stats = item.xpath('//td[@class="wisbb_priorityColumn wisbb_selected"]/text()').extract()
            players = playernames[::2]
            print(len(stats))
            print(len(players))
            gameData['Name'] = players
            gameData['Touches'] = stats
            gameData['Team'] = team
            print('=======================================================================\n')


m = EPLSpider
for i in range(1,PAGES):
    currenturl = url + str(i)
    response = pageData[currenturl]
    m.parsePlayerStats(EPLSpider,response)


# In[ ]:




# In[ ]:

teamstandingsurl = "http://www.foxsports.com/soccer/standings?competition=1"

r = requests.get(teamstandingsurl)
response = TextResponse(r.url, body=r.text, encoding='utf-8')
pageTeamData[currenturl] = response   

class TeamSpider(Spider):
    name = 'ManSpider'
    allowed_domains = ["foxsports.com"]

    def parseTeamStats(self, response):
        hxs = Selector(response)
        items = hxs.xpath('//table')
        my_item = dict()
        for item in items:
            print(item)
            

            
            
t = TeamSpider
t.parseTeamStats(TeamSpider, )



# In[ ]:




# In[ ]:



