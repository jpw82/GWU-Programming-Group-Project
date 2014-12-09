GWU-Programming-Group-Project
=============================

group project for web scraping and analysis
Programming for Analytics - DNSC 6211
Group Project

John Yoo
Josh Winters
Nayden Hitchev
Ben Aronin


Workflow Summary/README
Our analytical workflow uses the following programs and packages:
Python 2.7
Modules: brscraper, pandas, numpy, matplotlib, MySQLdb
R 3.1
Packages: Shiny, ggplot2
MySQL
Twitter API (requires Twitter account and API access tokens)

With those programs and packages installed:
First you must run brscraper.py which can be downloaded from the following GitHub account;
https://github.com/andrewblim/br-scraper

Run bigscrapeV5.py
On our computers, the scraping usually takes approximately 5 minutes.
https://github.com/jpw82/GWU-Programming-Group-Project/blob/master/bigscrapeV5.py
This will save several csv files to your working directory

Start a MySQL instance with root MySQL access privileges; create a database named “MLB”
When that is complete, run mlb2014.py
https://github.com/jpw82/GWU-Programming-Group-Project/blob/master/mlb2014.py
This will create the main table mlbdf2014 as a MySQL table.
Also adds several other tables for future work.

When that is complete, run twitterMod.py
This twitter mod is called in the script that was used to scrape twitter five times for sentiment analysis.
https://github.com/jpw82/GWU-Programming-Group-Project/blob/master/twitterMod.py
The script mlbtwitter.py is the code used to scrape twitter over 5 consecutive days.;
https://github.com/jpw82/GWU-Programming-Group-Project/blob/master/mlbtwitter.py

Each day a csv file was saved with the data from that day.
Data from each of the five scrapes was combined in the NovTwitterScore.py file;
https://github.com/jpw82/GWU-Programming-Group-Project/blob/master/NovTwitterScore.py
This file will create a csv in your working directory, however the csv is also already uploaded to GitHub and can be found at;
https://github.com/jpw82/GWU-Programming-Group-Project/blob/master/NovTwitterScore.csv 

When that is complete, run MLB Analysis Script.R
At the top of the script, where it establishes the connection to SQL, make sure you enter the credentials and password for your local SQL server
In the “read_csv” section, make sure you enter the file path of the Twitter CSV file that was created earlier in Python
There should now be a Shiny interactive object active.  You can open up the server.r and ui.r files and run the application.
Make sure that the file paths for mlbdf2014.csv, R2Table.csv, and NovTwitterScore.csv are addressed to the correct folder/working directory.
R files needed are ui.R and server.R
https://github.com/jpw82/GWU-Programming-Group-Project/blob/master/server.R
https://github.com/jpw82/GWU-Programming-Group-Project/blob/master/ui.R

You may select different tabs to show different outputs of data
When that is completed, you can go into your working directory to see a log file of all the user inputs captured from the Wins Predictor tool.

