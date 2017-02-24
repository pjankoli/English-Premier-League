
# coding: utf-8

# In[2]:

import pandas as pd
import numpy as np
import math
import statsmodels.discrete.discrete_model as sm
from scipy.stats import poisson
import json
import csv
import urllib
import pandas.io.data as web
import datetime
from datetime import timedelta
import matplotlib
import matplotlib.pyplot as plt
from sklearn.linear_model.logistic import LogisticRegression
import statsmodels.formula.api as smf
get_ipython().magic('matplotlib inline')


SeasonData = 'D:\\EPL Data\\E16.csv'

listTeams16 = "Arsenal	Aston Villa	Bournemouth	Chelsea	Crystal Palace	Everton	Leicester	Liverpool	Man City	Man United	Newcastle	Norwich	Southampton	Stoke	Sunderland	Swansea	Tottenham	Watford	West Brom	West Ham"
Teams = listTeams16.split('	')
data = pd.read_csv(SeasonData, index_col=1, parse_dates=True, delimiter=',', dayfirst=True)
season = data.ix[:,1:14]


modellingDataColumns = list()
for t in Teams:
    modellingDataColumns.append(t + "A")
    modellingDataColumns.append(t + "D")

modellingDataColumns.append("Goals")    
modellingDataColumns.append("Home")
modellingDataColumns.append("Shots")
modellingDataColumns.append("ShotsOnTarget")
    
feat = pd.DataFrame(columns=modellingDataColumns)
i = 0
for r in season.iterrows():
    homeTeamAttack = r[1]["HomeTeam"] + "A"
    homeTeamDefence = r[1]["HomeTeam"] + "D"
    awayTeamAttack = r[1]["AwayTeam"] + "A"
    awayTeamDefence = r[1]["AwayTeam"] + "D"
    homeGoals = r[1]["FTHG"]
    awayGoals = r[1]["FTAG"]
    homeShots = r[1]["HS"]
    awayShots = r[1]["AS"]
    homeShotsOnTarget = r[1]["HST"]
    homeShotsOnTarget = r[1]["AST"]
    
    row = [0] * 44
    feat.loc[i] = row
    feat.loc[i+1] = row
    
    #i -> Home record
    #i+1 -> Away record
    
    # Home advantage
    feat.loc[i]["Home"] = 1
    feat.loc[i]["Shots"] = homeShots
    feat.loc[i+1]["Shots"] = awayShots
    feat.loc[i]["ShotsOnTarget"] = homeShotsOnTarget
    feat.loc[i+1]["ShotsOnTarget"] = homeShotsOnTarget
    
    if (r[1]["FTR"] == "H"):
        #print(str(i) + " " + homeTeamAttack)
        feat.loc[i][homeTeamAttack] = 1
        feat.loc[i]["Goals"] = homeGoals
        feat.loc[i+1]["Goals"] = -1*awayGoals
    elif (r[1]["FTR"] == "A"):
        #print(str(i) + " " + awayTeamAttack)
        feat.loc[i+1][awayTeamAttack] = 1
        feat.loc[i]["Goals"] = -1*homeGoals
        feat.loc[i+1]["Goals"] = awayGoals
    else:
        #print(str(i) + " " + homeTeamAttack + " " + awayTeamAttack)
        feat.loc[i][awayTeamAttack] = -1
        feat.loc[i+1][awayTeamAttack] = -1
        feat.loc[i]["Goals"] = homeGoals
        feat.loc[i+1]["Goals"] = awayGoals
        
    i = i+2

 
#smf.ols(formula= "Goals ~ Home", data=feat).fit().summary()
#feat[~feat.applymap(np.isreal).all(1)]
smf.ols(formula= "Goals ~ Home+ShotsOnTarget", data=feat).fit().summary()   


# In[2]:




# In[ ]:



