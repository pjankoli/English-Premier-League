
# coding: utf-8

# In[45]:

from bs4 import BeautifulSoup
import pandas as pd
import urllib
domain = "https://www.fifaindex.com"

url = "https://www.fifaindex.com/players/1/?position=0&league=13"
r = urllib.urlopen(url).read()
soup = BeautifulSoup(r, "lxml")


# In[48]:

playerURLs = list()

tabtab = soup.find("table", {"class" : "table table-striped players"})
for row in tabtab.findAll('tr'):
    col = row.findAll('td')
    if(len(col) > 2):
        playerURLs.append(domain + col[0].findAll('a')[0]['href'])
        print(col[0].findAll('a')[0]['href'])
        print("Name: ", col[0].findAll('a')[0]['title'])
        print("Overall: ", col[2].findAll('span')[0].getText())
        print("Potential: ", col[2].findAll('span')[1].getText())
        print("Age: ", col[5].getText())
        print("Team: ",col[6].findAll('a')[0]['title'])
        print("----------")
        


# In[49]:

playerURLs


# In[ ]:



