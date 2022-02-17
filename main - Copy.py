#Code from youtube source to extract Twitter posts
import tweepy
auth = tweepy.OAuthHandler("Omiemks7GHNo9QO3WuNZxrbaW", "cCChIK5zIFOT1qDJ1ZjjmyQLh565yTveIeHBCQBrrMEwQCTlmA")
auth.set_access_token("1494032499625840653-PfkRAdSxA05vUZdklE0SIOGm0nGBst", "d7VXRNRvOsUWwweQTXDGYUebRaxIrEHMJ9FNHweFYQyIj")

api = tweepy.API(auth)
public_tweets = api.home_timeline()

for tweet in public_tweets:
    print(tweet.text)
