# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 20:26:39 2014

@author: jpw82
"""

# This is the link that formed the basis for what we did in class
# http://jeffreybreen.wordpress.com/2011/07/04/twitter-text-mining-r-slides/
# It is a great link to learn how to do the same thing in R

import twitterMod as tm
import pandas as pd

# Get negative and positive words into lists; we do this only once
teams = ["Dbacks","Braves","Orioles","RedSox","Cubs","whitesox","Reds","Indians","Rockies","tigers",
         "astros","Royals","Angels","Dodgers","Marlins","Brewers","Twins","Mets","Yankees","Athletics",
         "Phillies","Pirates","Padres","SFGiants","Mariners","Cardinals","RaysBaseball","Rangers","BlueJays","Nationals"]

teamabrv = ["ARI","ATL","BAL","BOS","CHC","CHW","CIN","CLE","COL","DET",
         "HOU","KCR","LAA","LAD","MIA","MIL","MIN","NYM","NYY","OAK",
         "PHI","PIT","SDP","SFG","SEA","STL","TBR","TEX","TOR","WSN"]
         
(negative, positive) = tm.getWordLists()


teamtsentscore = []
teamtwitterscore = []

for team in teams:
    status_texts  = tm.getTwitterData('@[team]')
    lowered_texts = tm.getLowerCaseText(status_texts)
    cleanedTweets = tm.getCleanedTweets(lowered_texts)
    sentscore       = tm.GetSentimentScores(cleanedTweets, negative, positive)
    twitterscore     = tm.getTwitterScore(sentscore)
    teamtsentscore.append(sentscore)
    teamtwitterscore.append(twitterscore)
    
mlbNovTwitter5 = pd.DataFrame(teamtwitterscore, index = teamabrv)
mlbNovTwitter5 = mlbNovTwitter5.rename(columns = {0:"NovTwitScore"})

mlbNovTwitter5.to_csv("mlbNovTwitter5.csv")
