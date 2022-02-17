import hashlib
from socket import *
import sys
import wolframalpha
from ServerKeys import *
from cryptography.fernet import Fernet
import os
import pickle

# 1. Receives question payload from the client
if (len(sys.argv) == 5) and (sys.argv[1] == "-sp") and (sys.argv[3] == "-z"):

    serverPort = int(sys.argv[2])
    socketSize = int(sys.argv[4])
    serverIP = "192.168.1.34"

    # print("serverPort:", serverPort)
    # print("socketSize:", socketSize)

    # Create TCP welcoming socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    print("[Server 01] - Created socket at ", serverIP, " on port ", serverPort)

    # Server begins listening for incoming TCP requests
    serverSocket.listen(1)
    print("[Server 02] - Listening for client connections")

    # Loop forever
    while True:
        # server waits on accept() for incoming requests, new socket created on return
        connectionSocket, address = serverSocket.accept()
        print("[Server 03] - Accepted client connection from ", address, " on port ", serverPort)

        # receive payload from socket
        unpickle_questionPayload = connectionSocket.recv(socketSize)
        print("[Server 04] - Received data:", unpickle_questionPayload)

        # print("Question:", question)

        key, encryptQues, md5hash = pickle.loads(unpickle_questionPayload)
        print("[Server 05] - Decrypt Key:", key)
        # print("key:", key)
        # print("encryptQues:", encryptQues)
        # print("md5hash:", md5hash)

        # retrieve encryption key
        decryptKey = Fernet(key)

        questionChecksum = hashlib.md5(encryptQues)
        if questionChecksum.digest() == md5hash:
            decryptQues = decryptKey.decrypt(encryptQues.decode("utf-8").encode()).decode("utf-8")
            print("[Server 06] - Plain Text:", decryptQues)

            # print("decryptQues:", decryptQues)
            # print("md5hash:", md5hash)

            # Find a response to the question
            # Code for how to connect to wolframalpha found on geeksforgeeks.com
            # https://www.geeksforgeeks.org/python-create-a-simple-assistant-using-wolfram-alpha-api/
            wolfclient = wolframalpha.Client(wolframID)
            print("[Server 08] - Sending question to Wolframalpha")
            result = wolfclient.query(decryptQues)

            try:
                answer = next(result.results).text
                print("[Server 09] - Received answer from Wolframalpha:", answer)
                #print("Answer:", answer)
            except StopIteration:
                print("Error: Invalid Question, WolframAlpha cannot answer")
                break

            fernet = Fernet(key)
            encryptAnswer = fernet.encrypt(answer.encode())

            md5hashAnswer = hashlib.md5(encryptAnswer)

            # Answer Payload: Answer text (encrypted), MD5 hash of encrypted answer text
            answerPayload = tuple((encryptAnswer, md5hashAnswer.digest()))
            answerPayload = pickle.dumps(answerPayload)

            connectionSocket.send(answerPayload)

        connectionSocket.close()

else:
    print("ERROR: Invalid Input")


# 2. Parses question payload

# 3. Sends question text to IBM Watson via API call

# 4. Receives speech voice file from IBM Watson

# 5. Speaks out question

# 6. Sends question to WolframAlpha engine via API call

# 7. Receives answer from WolframAlpha engine

# 8. Builds answer payload

# 9. Sends answer payload to client via socket interface
