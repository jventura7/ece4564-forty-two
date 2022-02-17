#Code from youtube source to extract Twitter posts
from clientKeys import *
import tweepy
auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)
public_tweets = api.home_timeline()

for tweet in public_tweets:
    if "#ECE4564T14" in tweet.text:
        print(tweet.text)
