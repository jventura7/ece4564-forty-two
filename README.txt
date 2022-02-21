CLIENT AND SERVER INITIALIZATION:
Client - In order to initialize the, the user must specify the server IP, port number, and the socket size. The server IP is the IP address of the Raspberry Pi, the port number does not matter what it is as long the server and client share the same port number, and the socket size is initialized as 1024. 
Server - In order to initialize the server, the user must specify the port and the socket size. The port and socket size must be the same number used by the client.


LIBRARIES:

Tweepy - Tweepy was used to access the Twitter API. More specifically, this library allowed us to grab data from our Twitter account and manipulate it in our python files. Functions such as tweepy.api allowed us to grab our api with the specific keys to our account and home_timeline() gave us the ability to store information from our live feed.
WolframAlpha - WolframAlpha library was used to set the client with our key and send questions to the api. query() allowed us to send a string message for WolframAlpha to answer and results() gave us the answer to that specific question.
Cryptography - This library allowed us to encrypt and decrypt the question that we retrieved from twitter. We used this library to obtain an encryption and decryption key which then allowed us to encrypt and decrypt the question. 
Hashlib - The hashlib library allowed us to come up with our md5 hash used in order to verify the checksum across the client and server
Pickle - The pickle library was used to send and receive the payload sent across the client and server. Since a tuple is not able to be sent through a socket, pickle allowed us to successfully pass this data from the client and read it from the server. 

OTHER:

To clarify, the code will continue to grab new tweets as long as the user keeps specifying so. If they say no, the program will stop. Anything else will be treated as an error and they will get another chance to retype their answer. 


