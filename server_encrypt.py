import sys
import wolframalpha
from socket import *
from serverKeys import *
from cryptography.fernet import Fernet
import os

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

        # receive payload from socket
        payload = connectionSocket.recv(socketSize).decode()
        # print("Question:", question)

        key, encryptQues, md5hash = payload
        # retrieve encryption key

        decryptQues = key.decrypt(encryptQues.encode())
        print(decryptQues)
        print(md5hash)


        # Find a response to the question
        wolfclient = wolframalpha.Client(wolframID)
        print("Question sent, waiting for response...")
        result = wolfclient.query(question)

        try:
            answer = next(result.results).text
            print("Answer:", answer)
        except StopIteration:
            print("Error: Invalid Question, WolframAlpha cannot answer")
            break;

        connectionSocket.send(answer.encode())

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