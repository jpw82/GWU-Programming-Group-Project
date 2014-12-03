"""
Created on Mon Nov 24 13:21:33 2014

@author: jpw82
"""

import numpy as np
import pandas as pd

###get an average twitter score for each team for the last week
####start by importing the data and put it all into a data frame

day1 = pd.DataFrame.from_csv("mlbNovTwitter.csv")
day2 = pd.DataFrame.from_csv("mlbNovTwitter2.csv")
day3 = pd.DataFrame.from_csv("mlbNovTwitter3.csv")
day4 = pd.DataFrame.from_csv("mlbNovTwitter4.csv")
day5 = pd.DataFrame.from_csv("mlbNovTwitter5.csv")

teams = ["Dbacks","Braves","Orioles","RedSox","Cubs","whitesox","Reds","Indians","Rockies","tigers",
         "astros","Royals","Angels","Dodgers","Marlins","Brewers","Twins","Mets","Yankees","Athletics",
         "Phillies","Pirates","Padres","SFGiants","Mariners","Cardinals","RaysBaseball","Rangers","BlueJays","Nationals"]

teamabrv = ["ARI","ATL","BAL","BOS","CHC","CHW","CIN","CLE","COL","DET",
         "HOU","KCR","LAA","LAD","MIA","MIL","MIN","NYM","NYY","OAK",
         "PHI","PIT","SDP","SFG","SEA","STL","TBR","TEX","TOR","WSN"]

teamabrv2 = np.array(teamabrv)
   
twittscore = day1.join(day2)
twittscore = twittscore.join(day3, rsuffix = 3).join(day4, rsuffix = 4).join(day5, rsuffix = 5)

twittscore = twittscore.rename(columns = {"NovSentScore":"day1",
                                          "NovTwitScore":"day2",
                                          "NovTwitScore3":"day3",
                                          "NovTwitScore4":"day4",
                                          "NovTwitScore5":"day5"})
                                          
twittscore = twittscore.transpose()

avgtwittscore = []

for i in teamabrv:
    avg = twittscore[i].mean().round()
    avgtwittscore.append(avg)

NovTwitterScore = pd.DataFrame(data = avgtwittscore)
NovTwitterScore = NovTwitterScore.set_index(keys = teamabrv2).rename(
columns = {0:"NovTwitterScore"})

NovTwitterScore.to_csv("NovTwitterScore.csv")

                                          
