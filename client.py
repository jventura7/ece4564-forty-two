
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
import hashlib
from ClientKeys import *
from socket import *
from cryptography.fernet import Fernet
import pickle

if (len(sys.argv) == 7) and (sys.argv[1] == "-sip") and (sys.argv[3] == "-sp") and (sys.argv[5] == "-z"):

    serverIP = sys.argv[2]
    serverPort = int(sys.argv[4])
    socketSize = int(sys.argv[6])
    print("serverIP:", serverIP)
    print("serverPort:", serverPort)
    print("socketSize:", socketSize)

    print("[Client 01] - Connecting to " + str(serverIP) + " on port " + str(serverPort))

    # code from "HACK ANON" YouTube Channel, Video: Twitter Api with python | example tutorial to get tweets
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth)
    public_tweets = api.home_timeline()

    tweetStr, hashtag = "", "#ECE4564T14"

    print("[Client 02] - Listening for tweets from Twitter API that contain questions")

    for tweet in public_tweets:
        if hashtag in tweet.text:
            # print(tweet.text)
            tweetStr = tweet.text
            break

    question = tweetStr.replace(hashtag, "")
    question = question.lstrip()
    question = question.rstrip()

    if len(question) == 0:
        print("Error: No question asked, retry with question + hashtag")
    else:

        print("[Client 03] - New question found:", question)

        # encryption key
        key = Fernet.generate_key()
        fernet = Fernet(key)

        # Encrypt question using python encryption library
        encryptQues = fernet.encrypt(question.encode())

        # encode encrypted question using md5 hash
        md5hash = hashlib.md5(encryptQues)

        # Construct question payload
        # Encrypt/Decrypt Key
        # Question text (encrypted)
        # MD5 hash of encrypted question text
        questionPayload = tuple((key, encryptQues, md5hash.digest()))

        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverIP, serverPort))

        request = question

        # No need to attach server name, port
        # clientSocket.send(request.encode())
        questionPayload = pickle.dumps(questionPayload)
        clientSocket.send(questionPayload)

        answerPayload = clientSocket.recv(socketSize)

        #answer = clientSocket.recv(socketSize).decode()
        #print("Answer:", answer)

        encryptAnswer, md5hashAnswer = pickle.loads(answerPayload)

        decryptAnswer = fernet.decrypt(encryptAnswer.decode("utf-8").encode())
        print("[Client 11] - Plain Text:", decryptAnswer)

        clientSocket.close()

else:
    print("ERROR: Invalid Input")


