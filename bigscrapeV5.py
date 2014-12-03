# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 14:02:37 2014

@author: jpw82
"""


import brscraper
import pandas as pd
import numpy as np
import matplotlib

scraper = brscraper.BRScraper()

teams = ["ARI","ATL","BAL","BOS","CHC","CHW","CIN","CLE","COL","DET",
         "HOU","KCR","LAA","LAD","MIA","MIL","MIN","NYM","NYY","OAK",
         "PHI","PIT","SDP","SFG","SEA","STL","TBR","TEX","TOR","WSN"]

teamdict = {}

for ix, team in enumerate(teams):
  teamdict[team] = scraper.parse_tables("/teams/tgl.cgi?team=%s&t=b&year2014=" % (team))


DF2014 = pd.DataFrame.from_dict(data = teamdict, orient = "index")


# example format for selecting a specific team , game and then stat from the master data frame

DF2014["team_batting_gamelogs"]["ARI"][5]["Rslt"]

#should return the result of the 6th game of the season for the arizona cardinals, L, 5-8


## now go through the DF2014 data frame and pull out the home run and win/loss/score data 
## for each team and game

teamlist = list(range(30))
games = list(range(162))

stolen = {}
strikeouts = {}
hits = {}
doubles = {}
triples = {}
homeruns = {}
results = {}
WinLoss = {}

for ix, team in enumerate(teams):
        stolen[team] = []
        strikeouts[team] = []
        hits[team] = []
        doubles[team] = []
        triples[team] = []
        homeruns[team] = []
        results[team] = []
        for j in games:
            stolen[team].append(DF2014["team_batting_gamelogs"][team][j]["SB"])
            strikeouts[team].append(DF2014["team_batting_gamelogs"][team][j]["SO"])
            hits[team].append(DF2014["team_batting_gamelogs"][team][j]["H"])
            doubles[team].append(DF2014["team_batting_gamelogs"][team][j]["2B"])
            triples[team].append(DF2014["team_batting_gamelogs"][team][j]["3B"])
            homeruns[team].append(DF2014["team_batting_gamelogs"][team][j]["HR"])
            results[team].append(DF2014["team_batting_gamelogs"][team][j]["Rslt"])

###Special loop to seperate the result column into seperate columns for result and score#####      
for ix, team in enumerate(teams):
    WinLoss[team] = []
    for j in games:
        parts = results[team][j].strip().split(",")
        WinLoss[team].append(parts)

Wintable = pd.DataFrame()
for k,v in WinLoss.items():
    for i, each in enumerate(v):
        # name the columns to whatever you want
        Wintable['{} {}'.format(k,'Result')] = [r[0] for r in v]
        Wintable['{} {}'.format(k,'Scores')] = [r[1] for r in v]

cols = Wintable.columns.values
cols = sorted(list(cols))
Wintable = Wintable[cols]

#####################################
SBtable = pd.DataFrame(stolen)
SOtable = pd.DataFrame(strikeouts)
Hitstable = pd.DataFrame(hits)
Doubletable = pd.DataFrame(doubles)   
Tripletable = pd.DataFrame(triples)        
HRtable = pd.DataFrame(homeruns)

###################################################

                    
##################################################
SBtable.to_csv("stolenbases2014.csv")
SOtable.to_csv("strikeouts2014.csv")
Hitstable.to_csv("hits2014.csv")
Doubletable.to_csv("doubles2014.csv")   
Tripletable.to_csv("triples2014.csv")       
HRtable.to_csv("homeruns2014.csv")
Wintable.to_csv("wins2014.csv")


####################################################


         
         
