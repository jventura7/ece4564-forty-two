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

    print("serverPort:", serverPort)
    print("socketSize:", socketSize)

    # Create TCP welcoming socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))

    # Server begins listening for incoming TCP requests
    serverSocket.listen(1)
    print("The server is ready to receive")

    # Loop forever
    while True:
        # server waits on accept() for incoming requests, new socket created on return
        connectionSocket, address = serverSocket.accept()

        # read bytes from socket
        # question = connectionSocket.recv(socketSize).decode()
        # print("Question:", question)

        # receive payload from socket
        payload = connectionSocket.recv(socketSize)
        # print("Question:", question)

        key, encryptQues, md5hash = pickle.loads(payload)
        print("key:", key)
        print("encryptQues:", encryptQues)
        print("md5hash:", md5hash)

        # retrieve encryption key
        decryptKey = Fernet(key)

        decryptQues = decryptKey.decrypt(encryptQues.decode("utf-8").encode())
        print("decrypyQues:", decryptQues)
        print("md5hash", md5hash)

        # Find a response to the question
        # Code for how to connect to wolframalpha found on geeksforgeeks.com
        # https://www.geeksforgeeks.org/python-create-a-simple-assistant-using-wolfram-alpha-api/
        wolfclient = wolframalpha.Client(wolframID)
        print("Question sent, waiting for response...")
        result = wolfclient.query(decryptQues)

        try:
            answer = next(result.results).text
            # print("Answer:", answer)
        except StopIteration:
            print("Error: Invalid Question, WolframAlpha cannot answer")
            break

        #connectionSocket.send(answer.encode())

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
