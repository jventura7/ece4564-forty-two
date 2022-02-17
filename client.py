
# 1. Captures Tweet and extracts question

# 2. Builds question payload

# 3. Sends question payload to the server via socket interface

# 4. Receives and parses answer payload

# 5. Sends answer text to IBM Watson via API call

# 6. Receives speech voice file from IBM Watson

# 7. Speaks out answer

# 8. Displays answer on monitor


#Code from youtube source to extract Twitter posts
import tweepy
import sys
from ClientKeys import *
from socket import *


auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)
public_tweets = api.home_timeline()

tweetStr = ""

hashtag = "#ECE4564T14"

for tweet in public_tweets:
    if hashtag in tweet.text:
        #print(tweet.text)
        tweetStr = tweet.text
        break

question = tweetStr.replace(" " + hashtag, "", 1)

print("Question:", question)

if (len(sys.argv) == 7) and (sys.argv[1] == "-sip") and (sys.argv[3] == "-sp") and (sys.argv[5] == "-z"):

    serverIP = sys.argv[2]
    serverPort = sys.argv[4]
    socketSize = sys.argv[6]
    print("serverIP:", serverIP)
    print("serverPort:", serverPort)
    print("socketSize:", socketSize)

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverIP, serverPort))

    request = question

    # No need to attach server name, port
    clientSocket.send(request.encode())

    received = clientSocket.recv(1024).decode()

    clientSocket.close()

else:
    print("ERROR: Invalid Input")


