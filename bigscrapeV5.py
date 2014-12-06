# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 14:02:37 2014

@author: jpw82
"""


import brscraper
import pandas as pd
import numpy as np

###define scraper function
scraper = brscraper.BRScraper()

###example scrape for one team 
balt = scraper.parse_tables("teams/tgl.cgi?team=BAL&t=b&year=2014")


###list of team abbreviations
teams = ["ARI","ATL","BAL","BOS","CHC","CHW","CIN","CLE","COL","DET",
         "HOU","KCR","LAA","LAD","MIA","MIL","MIN","NYM","NYY","OAK",
         "PHI","PIT","SDP","SFG","SEA","STL","TBR","TEX","TOR","WSN"]

####Empty dictionary to store all dat
teamdict = {}

for i, team in enumerate(teams):
  teamdict[team] = scraper.parse_tables("/teams/tgl.cgi?team=%s&t=b&year2014=" % (team))

####Example queery of teamdict for team, game and statistic
teamdict["ARI"]["team_batting_gamelogs"][1]["Rslt"]


###convert teamdict to data frame
DF2014 = pd.DataFrame.from_dict(data = teamdict, orient = "index")

#should return the result of the 6th game of the season for the arizona cardinals, L, 5-8


###Now I ultimatley need one data table with each teams season avg for the 6 offensive stats 
### and winning percentage. So I make individual tables for each stat for all teams to compute avg's

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

for i, team in enumerate(teams):
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
for i, team in enumerate(teams):
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


         
         
