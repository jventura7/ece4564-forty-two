
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
    #print("serverIP:", serverIP)
    #print("serverPort:", serverPort)
    #print("socketSize:", socketSize)

    print("[Client 01] - Connecting to " + str(serverIP) + " on port " + str(serverPort))

    # code from "HACK ANON" YouTube Channel, Video: Twitter Api with python | example tutorial to get tweets
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    loop = True
    while loop:
        keepLoop = input('Look for tweets? Y/N: ')
        if keepLoop == 'Y':
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
                print("[Client 05]  - Generated Encryption Key:", key)

                fernet = Fernet(key)

                # Encrypt question using python encryption library
                encryptQues = fernet.encrypt(question.encode())
                print("[Client 06] - Cipher Text: ", encryptQues)

                # encode encrypted question using md5 hash
                md5hash = hashlib.md5(encryptQues)

                questionPayload = tuple((key, encryptQues, md5hash.digest()))
                print("[Client 07] - Question Payload:", questionPayload)

                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect((serverIP, serverPort))

                # No need to attach server name, port
                pickle_questionPayload = pickle.dumps(questionPayload)

                print("[Client 08] - Sending question:", pickle_questionPayload)
                clientSocket.send(pickle_questionPayload)

                answerPayload = clientSocket.recv(socketSize)

                unpickle_answerPayload = pickle.loads(answerPayload)
                encryptAnswer, md5hashAnswer = unpickle_answerPayload
                print("[Client 09] - Received data:", unpickle_answerPayload)
                print("[Client 10] - Decrypt Key:", key)
                answerChecksum = hashlib.md5(encryptAnswer)
                if answerChecksum.digest() == md5hashAnswer:
                    decryptAnswer = fernet.decrypt(encryptAnswer.decode("utf-8").encode()).decode("utf-8")
                    print("[Client 11] - Plain Text:", decryptAnswer)
        elif keepLoop == 'N':
            print('Stopped program.')
            clientSocket.close()
            loop = False
        else:
            print("Invalid Response, type either Y/N")
else:
    print("ERROR: Invalid Input")


