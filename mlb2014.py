# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 17:10:27 2014

@author: Josh New
"""

import pandas as pd
import MySQLdb as myDB

##useful to have

teams = ["ARI","ATL","BAL","BOS","CHC","CHW","CIN","CLE","COL","DET",
         "HOU","KCR","LAA","LAD","MIA","MIL","MIN","NYM","NYY","OAK",
         "PHI","PIT","SDP","SFG","SEA","STL","TBR","TEX","TOR","WSN"]

games = list(range(162))


###import csv's into data frames
SBtable = pd.DataFrame.from_csv("stolenbases2014.csv")
SOtable = pd.DataFrame.from_csv("strikeouts2014.csv")
Hitstable = pd.DataFrame.from_csv("hits2014.csv")
Doubletable = pd.DataFrame.from_csv("doubles2014.csv")   
Tripletable = pd.DataFrame.from_csv("triples2014.csv")       
HRtable = pd.DataFrame.from_csv("homeruns2014.csv")
Wintable = pd.DataFrame.from_csv("wins2014.csv")

###send to MySQL for use in R




###calculate the winning percentage for each team and put it in a list


evenlist = list(range(0,60, 2))
teamwinpct = []

for i in evenlist:
    winpct = (sum(Wintable.icol(i)=="W")/float(162))
    teamwinpct.append(winpct)

##save it to a data frame with proper index

winpct2014 = pd.DataFrame(teamwinpct, index = teams)
winpct2014 = winpct2014.rename(columns = {0:"WinPct"}) 

#winpct2014.to_csv("winpct2014.csv") 

################Get the season average for each team for each stat

teamlist = list(range(30))

avglist = ["avgSB", "avgSO", "avgHits","avgDBL","avgTRPL","avgHRs"]

avgSB = SBtable.sum(0)/float(162)
avgSO = SOtable.sum(0)/float(162)
avgHits = Hitstable.sum(0)/float(162)
avgDBL = Doubletable.sum(0)/float(162)
avgTRPL = Tripletable.sum(0)/float(162)
avgHRs = HRtable.sum(0)/float(162)

avgSB = pd.DataFrame(avgSB)
avgSB = avgSB.rename(columns = {0:"avgSB"})
avgSO = pd.DataFrame(avgSO)
avgSO = avgSO.rename(columns = {0:"avgSO"})
avgHits = pd.DataFrame(avgHits)
avgHits = avgHits.rename(columns = {0:"avgHits"})
avgDBL = pd.DataFrame(avgDBL)
avgDBL = avgDBL.rename(columns = {0:"avgDoubles"})
avgTRPL = pd.DataFrame(avgTRPL)
avgTRPL = avgTRPL.rename(columns = {0:"avgTriples"})
avgHRs = pd.DataFrame(avgHRs)
avgHRs = avgHRs.rename(columns = {0:"avgHRs"})


###Join all these DFs into one to compare win % and offensive stats
mlbdf2014 = winpct2014.join(other = [avgSB,avgSO,avgHits,avgDBL,avgTRPL,avgHRs])

#mlbdf2014.to_csv("mlbdf2014.csv")
                
###MySQL instructions:
##at linux command prompt
#mysql -u root -p
#then: enter password
##at mysql prompt
#create database MLB;
#use MLB;
                
                
###send everything to MySQL for use in R


#connect to mySQL database



##ADJUST THESE PARAMETERS IF YOU ARE RUNNING THIS PROGRAM ON A NEW COMPUTER
dbConnect = myDB.connect(host='localhost',
                            user='root',
                            passwd='root',
                            db='MLB')  #database of this name must have already been created in mySQL

##create and define new database table
mlbdf2014.to_sql(con=dbConnect,
                name='mlbdf2014',
                if_exists='replace',
                flavor='mysql')

SBtable.to_sql(con=dbConnect,
                name='SBtable',
                if_exists='replace',
                flavor='mysql') 
                
SOtable.to_sql(con=dbConnect,
                name='SOtable',
                if_exists='replace',
                flavor='mysql') 
                
Hitstable.to_sql(con=dbConnect,
                name='Hitstable',
                if_exists='replace',
                flavor='mysql') 
                
Doubletable.to_sql(con=dbConnect,
                name='Doubletable',
                if_exists='replace',
                flavor='mysql') 
                
Tripletable.to_sql(con=dbConnect,
                name='Tripletable',
                if_exists='replace',
                flavor='mysql')
                
HRtable.to_sql(con=dbConnect,
                name='HRtable',
                if_exists='replace',
                flavor='mysql') 
                
Wintable.to_sql(con=dbConnect,
                name='Wintable',
                if_exists='replace',
                flavor='mysql') 

#close the cursor and the database connection

dbConnect.close()                
                
                
