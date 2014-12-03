# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 20:15:52 2014

@author: jpw82
"""

def getTwitterData(searchTerm):
    
    import twitter
 
    CONSUMER_KEY = 'WmJndGRvbL9bxtn5NMJrFx1DH'
    CONSUMER_SECRET ='v9VAGAtMufZ7F4U52r1JQvsxU21zvfzTHs7glwQkyygQAiKKR0'
    OAUTH_TOKEN = '2848989279-5a5AwK32EbQG18LDirbQacHkmei7BLsjw9UGpOZ'
    OAUTH_TOKEN_SECRET = 'NBDOrGxxa7HooW7liieGos04mh47dssl3r89FoKZ7JFwT'
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN,
                               OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY,
                               CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)
    
    # Nothing to see by displaying twitter_api except that it's now a
    # defined variable
    print twitter_api
    
    searchCount = 180 # The number of tweets you want ... you never get that !
    
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q=searchTerm, count=searchCount)
    statuses = search_results['statuses']
    
    # Iterate through 5 more batches of results by following the cursor
    
    for _ in range(5):
        print "Length of statuses", len(statuses)
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            print "That's all folks for ...", searchTerm
            break
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        # kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
	# This was in the original code piece, see link below
	# http://nbviewer.ipython.org/github/ptwobrussell/Mining-the-Social-Web/blob/master/ipython_notebooks/Chapter1.ipynb        
	# I just broke the previous statement into two parts shown below
        # It may be easier for some folks to understand
        # Also, I start from the 0 position instead of the 1 position to
        # split based on "&"; make sure you explore the data in the
        # variable explorer to understand what is going on -- Raj
        myKVs = [ kv.split('=') for kv in next_results[1:].split("&") ]
        myStrippedKVs = [ [str(pp[0]), str(pp[1])] for pp in myKVs]
        kwargs = dict(myStrippedKVs)    
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
    
    status_texts = [ status['text'] for status in statuses ]
    return status_texts
    
    
def getWordLists():
    negative = [line.strip() for line in open('negative-words.txt')]
    negative = [n for n in negative if n != [] ]
    negative = [n for n in negative if n != '' ]
    negative = [n for n in negative if n[0] != ';']
    
    positive = [line.strip() for line in open('positive-words.txt')]
    positive = [n for n in positive if n != [] ]
    positive = [n for n in positive if n != '' ]
    positive = [n for n in positive if n[0] != ';']
 
    return positive, negative
    
def remove_punctuation(s):
    punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    s_sans_punct = ""
    for letter in s:
        if (letter not in punctuation) and (letter in "abcdefghijklmnopqrstuvwxyz "):
            s_sans_punct += letter
    return s_sans_punct
 
 
def getLowerCaseText(status_texts):
    lowered_texts = []
    for texts in status_texts:
        try: 
            mytext = str(texts.lower())
            lowered_texts.append(mytext)
        except:
            pass
    return lowered_texts
 
def getCleanedTweets(lowered_texts):
    cleanedTweets = []
    for text in lowered_texts:
        wordlist = str(text).split()
        wordlist_nopun = [ str(remove_punctuation(for_a_word)) for for_a_word in wordlist ]
        cleanedTweets.append(wordlist_nopun)
    return cleanedTweets
 
def GetSentimentScores(cleanedTweets, negative, positive):
    freqList = []
    for eachTweet in cleanedTweets:
        posScore = len(set(eachTweet) & set(positive))
        negScore = len(set(eachTweet) & set(negative))
        freqList.append(posScore-negScore)
    return freqList
 
def plotHist(freqList):
    import matplotlib.pyplot as plt
    plt.hist(freqList)
 
 
def getTwitterScore(freqList):
    veryNegative = len([x for x in freqList if x<=-2])
    veryPositive = len([x for x in freqList if x>=+2])
    twitterScore = 100 * (float (veryPositive) / (veryNegative + veryPositive))
    return round(twitterScore, 2)
 
 
