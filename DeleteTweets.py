#This script inspired by Chris Albon's script/gist "tweet_deleting_script.py":
#    https://gist.github.com/chrisalbon/b9bd4a6309c9f5f5eeab41377f27a670
import json
import tweepy
from datetime import datetime

# CONSTANTS
#These string values are specific to *your* Twitter account and Twitter app.
#You will need to register for a Twitter developer account,
#create a Twitter app, and give the app Read/Write permissions.
API_KEY = '396F006F-C66F-4B54-8479-990FFDEDB8AB'  
API_SECRET = '396F006F-C66F-4B54-8479-990FFDEDB8AB'  
ACCESS_TOKEN = '396F006F-C66F-4B54-8479-990FFDEDB8AB'
ACCESS_SECRET = '396F006F-C66F-4B54-8479-990FFDEDB8AB'

#You will need to "Download an archive of your data" from Twitter to get the "tweet.js" file.
TWEETS_FILE_PATH = 'C:/Users/You/Documents/Twitter Archive/data/tweet.js'
LIKE_COUNT_THRESHOLD = 1        #Delete tweets with less than X likes.
RETWEET_COUNT_THRESHOLD = 1     #Delete tweets with less than X retweets.
TWEET_DATE_THRESHOLD = datetime.fromisoformat('2020-01-01') #Delete tweets made before this date.

# Connect To Your Twitter Account via Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth,
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True,
                 retry_count=3,
                 retry_delay=5,
                 retry_errors=set([401, 404, 500, 503]))

#Open the "tweets" file from your Twitter archive.
with open(TWEETS_FILE_PATH, 'r', encoding='utf8') as tweetsFile:
    tweetsString = tweetsFile.read()
    characterPosition = tweetsString.find('[')

    if (characterPosition != -1):
        tweetsString = tweetsString[characterPosition:]
    
    jsonData = json.loads(tweetsString)
    #Iterate through the tweets.
    for tweets in jsonData:
        #Pull the id and date from the JSON data file.
        tweetId = tweets['tweet']['id']
        tweetDate = datetime.strptime(tweets['tweet']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

        #if the tweet is older than the threshold...
        if (tweetDate < TWEET_DATE_THRESHOLD):
            try:
                #Pull other up-to-the-moment meta data via tweepy (which uses the Twitter API).
                apiTweet = api.get_status(id=tweetId)
                likesCount = apiTweet._json['favorite_count']
                likedByMe = apiTweet._json['favorited']
                retweetCount = apiTweet._json['retweet_count']

                #...and the tweet has fewer likes than the threshold...
                if(likesCount < LIKE_COUNT_THRESHOLD):
                    #...and I didn't like/favorite the tweet...
                    if(likedByMe == FALSE):
                        #...and the tweet has fewer retweets than the threshold...
                        if(retweetCount < RETWEET_COUNT_THRESHOLD):
                            #...delete the tweet.
                            print(tweetDate.strftime("%d/%m/%Y %H:%M:%S"), 'Deleting', tweetId)
                            api.destroy_status(tweetId)
            except Exception as ex:
                print(ex)
