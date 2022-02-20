# Code from youtube source to extract Twitter posts
from clientKeys import *
from serverKeys import *
import tweepy
import wolframalpha

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
keepLooping = True
while keepLooping:
    keepGoing = input('Look for tweets? Y/N: ')
    if keepGoing == 'Y':
        api = tweepy.API(auth)
        public_tweets = api.home_timeline()
        tweetStr = ""
        hashtag = "#ECE4564T14"
        for tweet in public_tweets:
            if hashtag in tweet.text:
                tweetStr = tweet.text
                break

        question = tweetStr.replace(hashtag, "")
        question = question.lstrip()
        question = question.rstrip()
        if len(question) == 0:
            print("Error: No question asked retry with question + hashtag")
        else:
            print("Question:", question)
            # Find a response to the question
            wolfclient = wolframalpha.Client(wolframID)
            print("Question sent, waiting for response...")
            result = wolfclient.query(question)
            try:
                txtAnswer = next(result.results).text
                print("Answer:", txtAnswer)
            except StopIteration:
                print("Error: Invalid Question, WolframAlpha cannot answer")
        keepLooping = True
    elif keepGoing == 'N':
        print("Stopped program.")
        keepLooping = False
    else:
        print("Invalid Response, type either Y/N")
        keepLooping = True
