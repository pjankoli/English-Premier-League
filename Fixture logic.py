
# coding: utf-8

# In[73]:

import pandas as pd
import numpy as np
import math
import statsmodels.discrete.discrete_model as sm
import json
import urllib2
import random

standings_2016 = "2016Standings.csv"
standings_2015 = "2015Standings.csv"
comingfixtures = "comingfixtures.csv"


# In[74]:

resp = urllib.urlopen("http://api.football-data.org/v1/competitions/426/leagueTable")
html = resp.read().decode('utf8')
dataLeagueJson = json.loads(html)


# In[75]:

leagueTable = pd.DataFrame(columns=("Team", "Position"))
i = 0
for d in dataLeagueJson["standing"]:
    row =[d["teamName"], d["position"]]
    leagueTable.loc[i] = row
    i = i+1

teams = leagueTable["Team"].tolist()  
temp = leagueTable.set_index('Team').to_dict()
standings = temp["Position"]
fixtures = pd.DataFrame(columns=("Home", "Away"))

for j in range(0,10):
    t1 = random.choice(teams)
    teams.remove(t1)
    t2 = random.choice(teams)
    teams.remove(t2)
    row = list()
    row =[t1, t2]
    fixtures.loc[j] = row
    j = j+1

#fixtures.to_csv(comingfixtures, sep=',', encoding='utf-8')
fixtures = pd.read_csv(comingfixtures)
fixtures


# In[76]:

leagueTable2015 = pd.read_csv(standings_2015)
temp = leagueTable2015.set_index('Team').to_dict()
standings2015 = temp["Position"]

leagueTable2015


# In[77]:

bigFixtures = pd.DataFrame(columns=("Home", "Away"))


# In[78]:

#Home teams standings this season till date
fixtures["HS"] = fixtures['Home'].map(standings)

#Away teams standings this season till date
fixtures["AS"] = fixtures['Away'].map(standings)

#Diff
fixtures["Diff"] = abs(fixtures["HS"] - fixtures["AS"])

#Same stuff for last season
fixtures["LHS"] = fixtures['Home'].map(standings2015)
fixtures["LAS"] = fixtures['Away'].map(standings2015)
fixtures["LDiff"] = abs(fixtures["LHS"] - fixtures["LAS"])

fixtures


# In[81]:


#Constraints for current standings
bigFixtures1 = fixtures.loc[fixtures["Diff"] > 9 ]
bigFixtures2 = fixtures.loc[((fixtures["HS"] < 10) & (fixtures["AS"] < 10)) ]
bigFixtures3 = fixtures.loc[((fixtures["HS"] > 17) & (fixtures["AS"] > 17)) ]

#Constraints for last year's standings (Made them stricter)
bigFixtures4 = fixtures.loc[fixtures["LDiff"] > 12 ]
bigFixtures5 = fixtures.loc[((fixtures["LHS"] < 7) & (fixtures["LAS"] < 7)) ]
bigFixtures6 = fixtures.loc[((fixtures["LHS"] > 17) & (fixtures["LAS"] > 17)) ]

#Take last year's top 4
bigFixtures7 = fixtures.loc[(fixtures["LHS"] <= 4)]

bigFixtures = bigFixtures1.append(bigFixtures2).append(bigFixtures3).append(bigFixtures4).append(bigFixtures5).append(bigFixtures6).append(bigFixtures7)
bigFixtures.drop_duplicates(inplace=True)

bigFixtures


# In[ ]:



