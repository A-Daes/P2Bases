from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient

MONGO_HOST = "mongodb+srv://aegistk14104:aegistk14104@cc3040alv14104-dawge.mongodb.net/test?retryWrites=true"

WORDS = ['Guatemala']

CONSUMER_KEY = "cI88OHNZdVfDfQj2Umi4XkQDp"
CONSUMER_SECRET = "mgBk2z3l8Io0R124jcerfIDEtUjC0zd9m1Xx9ZNp4XXExK3h68"
ACCESS_TOKEN = "278872184-hHR5NcMEpaABQO5LJgKYujdD0ldNIdCNd62awxVz"
ACCESS_TOKEN_SECRET = "rT4LzrbKkvLcPawJH7WINpEfiUX80KQvlGPMzjtdspSst"


class StreamListener(tweepy.StreamListener):    
    #This is a class provided by tweepy to access the Twitter Streaming API. 

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            client = MongoClient(MONGO_HOST)
            
            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.twitterdb
    
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            
            #grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']

            #print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))
            
            #insert the data into the mongoDB into a collection called twitter_search
            #if twitter_search doesn't exist, it will be created.
            db.twitter_search.insert(datajson)
        except Exception as e:
           print(e)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)