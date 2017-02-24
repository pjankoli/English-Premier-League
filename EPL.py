
# coding: utf-8

# In[1]:

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
get_ipython().magic('matplotlib inline')


S1415 = 'D:\\EPL Data\\E15.csv'

listTeams = "Arsenal	Aston Villa	Burnley	Chelsea	Crystal Palace	Everton	Hull	Leicester	Liverpool	Man City	Man United	Newcastle	QPR	Southampton	Stoke	Sunderland	Swansea	Tottenham	West Brom	West Ham"
Teams = listTeams.split('	')
data = pd.read_csv(S1415, index_col=1, parse_dates=True, delimiter=',', dayfirst=True)
season = data.ix[:,1:6]
#factors = pd.DataFrame(columns=('Team', 'alpha - Home Goals scored', 'beta - Home Goals conceded', 'gamma - Away Goals scored', 'delta - Away Goals conceded'))
factors = pd.DataFrame(columns=('Team', 'alpha', 'beta', 'gamma', 'delta'))

season = season.ix[:190]


# In[2]:

i = 1
for t in Teams:
    homeResults = season.loc[(season['HomeTeam'] == t)]
    awayResults = season.loc[(season['AwayTeam'] == t)]
    homeAttack = homeResults['FTHG']
    homeDefence = homeResults['FTAG']
    alpha = list(homeAttack)
    beta = list(homeDefence)
    awayAttack = awayResults['FTAG']
    awayDefence = awayResults['FTHG']
    gamma = list(awayAttack)
    delta = list(awayDefence)
    if len(alpha) != len(beta):
        raise Exception('Check Alpha and Delta lengths for ', t)
    if len(gamma) != len(delta):
        raise Exception('Check Gamma and Delta lengths for ', t)    
    resAlpha = sm.Poisson(alpha,np.ones_like(alpha)).fit(disp=0)
    resBeta = sm.Poisson(beta,np.ones_like(beta)).fit(disp=0)
    resGamma = sm.Poisson(gamma,np.ones_like(gamma)).fit(disp=0)
    resDelta = sm.Poisson(delta,np.ones_like(delta)).fit(disp=0)
    
    allresults = [t, np.exp(resAlpha.params[0]), np.exp(resBeta.params[0]), np.exp(resGamma.params[0]), np.exp(resDelta.params[0])]
    factors.loc[i] = allresults
    i = i+1

factors


# In[3]:

homeResults = season.loc[(season['HomeTeam'] == 'QPR')]
awayResults = season.loc[(season['AwayTeam'] == 'QPR')]
homeGoals = homeResults['FTHG']
a = list(homeGoals)
awayGoals = awayResults['FTAG']
b = list(awayGoals)
c = a + b
res = sm.Poisson(c,np.ones_like(c)).fit()
print(res.params)
res.summary()


# In[ ]:




# In[4]:

season2 = data.ix[190:,1:]
secondHalfProb = pd.DataFrame(columns=('HomeTeam', 'AwayTeam', 'HomeWin', 'AwayWin', 'Draw', 'TotalProb', 'ActualResult', 'B365DrawOdds'))
seasonTest = season2.loc[season2['FTR'] == "D"]
it = 0
for index, row in seasonTest.iterrows():
    homeTeam = row['HomeTeam']
    awayTeam = row['AwayTeam']
    #Home
    varHome = factors.loc[(factors['Team'] == homeTeam)]
    aH = varHome['alpha']
    bH = varHome['beta']

    #Away
    varAway = factors.loc[(factors['Team'] == awayTeam)]
    gA = varAway['gamma']
    dA = varAway['delta']

    H = aH.iloc[0] * dA.iloc[0]
    A = gA.iloc[0] * bH.iloc[0]
    
    
    homeProb = list()
    for i in range(0,6):
        homeProb.append(poisson.pmf(i,H))

    awayProb = list()
    for i in range(0,6):
        awayProb.append(poisson.pmf(i,A))
    
    hwinP, awinP, dP = 0, 0, 0
    for h in range(0,6):
        for a in range(0,6):
            if h>a: hwinP += homeProb[h]*awayProb[a]*100
            elif h<a: awinP += homeProb[h]*awayProb[a]*100
            else: dP += homeProb[h]*awayProb[a]*100
    rowData =  [homeTeam, awayTeam, hwinP, awinP, dP, hwinP+awinP+dP, row['FTR'], row['B365D']]
    secondHalfProb.loc[it] = rowData
    it = it+1
 
secondHalfProb
    
    
            
        
    
    


# In[ ]:




# In[ ]:



