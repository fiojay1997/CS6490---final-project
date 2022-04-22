# CS6490---final-project
CS6490 UofU - final project. Team member: Steven, Leo, Kaijie

### running the auth server
- pip3 install flask
- pip3 install pyjwt
- python3 auth.py 
- hosted on 127.0.0.1:5000 port (either visit on browser or just do curl)

- 127.0.0.1:5000/auth gives you the login screen, password currently is hard coded to 'password', and username is anything, 
  this will be fixed later using a local file.
- a token with secrete key is authorized after login, use this to go further