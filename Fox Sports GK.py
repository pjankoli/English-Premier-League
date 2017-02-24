
# coding: utf-8

# In[2]:

from bs4 import BeautifulSoup
import pandas as pd
import urllib

url = 'http://www.foxsports.com/soccer/stats?competition=1&season=20160&category=GOALKEEPING'

r = urllib.request.urlopen(url).read()
soup = BeautifulSoup(r, "lxml")
print(type(soup))


# In[3]:

#columns = ["Name", "GP", "GS", "MP", "G","A", "SOG", "S", "YC", "RC"]
columns = list()

colcol = soup.find("thead", {"class" : "wisbb_tableHeader"})
cols = colcol.findAll(lambda tag: tag.name=='th')
for c in cols:
    columns.append(c.getText().strip())
    
print(columns)


# In[5]:

tabtab = soup.find("table", {"class" : "wisbb_standardTable"})

#rows = tabtab.findAll(lambda tag: tag.name=='tr')

def CheckBookings(x):
    if x > 3:
        return "Danger"
    else:
        return ""   
        

records = pd.DataFrame(columns=columns)
i = 0
for row in tabtab.findAll('tr'):
    rowData = list()
    col = row.findAll('td')
    if(len(col) > 2):
        tempName = col[0].findAll('span')[1].getText()
        name = " ".join(tempName.split(", ")[::-1])
        rowData.append(name)
        temp = col[1:]
        for t in temp:
            rowData.append((float(t.getText())))
        records.loc[i] = rowData    
        i = i+1

#records["Rate"] = records["G"].div(records["G"], axis='index')
#records["GRate"] = records["G"]/records["MP"]
#records["ARate"] = records["A"]/records["MP"]
#records["BookingFlag"] = pd.Series([CheckBookings(x) for x in records.YC], index=records.index)
records


# In[ ]:




# In[ ]:



