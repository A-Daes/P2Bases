from pymongo import *
import pprint
MONGO_HOST = MongoClient("mongodb+srv://aegistk14104:aegistk14104@cc3040alv14104-dawge.mongodb.net/test?retryWrites=true")
db = MONGO_HOST.twitterdb
tweets = db.twitter_search

post  = tweets.find_one()
pprint.pprint(post["text"])