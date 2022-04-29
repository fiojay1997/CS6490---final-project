# CS6490---final-project
CS6490 UofU - final project. Team member: Steven, Leo, Kaijie

## running the proof of concept models 
- python3 server.py to start the server
- python3 client.py to run the first client
- python3 client.py to run the second client
- input the names on both clients, (they should be identical, ie, one client called 'alice', and it want to talk to 'bob', the other client should be called 'bob')
- input selected number (5 digits +)
- send the message when key was encryption is done

## running the twitter API tests
- currently we don't really have the permission to run our secretes for accessing the API, but we were
  told it should be available two weeks later
- pip3 install tweepy 
- python3 twitter_msg.py 
- two clients are needed to run the test

### running the auth remote server
- pip3 install flask
- pip3 install pyjwt
- python3 auth.py 
- hosted on 127.0.0.1:5000 port (either visit on browser or just do curl)

- 127.0.0.1:5000/auth gives you the login screen, password currently is hard coded to 'password', and username is anything, 
  this will be fixed later using a local file.
- a token with secrete key is authorized after login, use this to go further

