import secrets
from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps
import os.path

app = Flask(__name__)
app.config['SECRETE_KEY']= 'eaa37fe1fa251109802ebb895f7830e3'

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token')
		if not token:
			return jsonify({'message': 'Token missing'}), 403
		try: 
			data = jwt.decode(token, app.config['SECRETE_KEY'])
		except:
			return jsonify({'message': 'Invalid token' }), 403

		return f(*args, **kwargs)
	return decorated

# this is an unprotected route, in our case we want to use this for exchanging user infos
@app.route('/unprotected')
def unprotected():
	return jsonify({'message': 'unprotected route has not been implemented yet'})

# this is a protected route, meaning the users have been authorized, use this to exchange files
@app.route('/protected')
@token_required
def protected():
	return jsonify({'message': 'protected route has not been implemented yet'})

@app.route('/auth')
def auth():
	auth = request.authorization
	if auth and auth.password == 'password':
		token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=100)}, app.config['SECRETE_KEY']) 
		return jsonify({'token': token})

	return make_response('Auth failed', 401, {'WWW-Authenticate': 'Basic realm="login required"'})

# since we are not using a database, the user info will directly stored in a file
@app.route('/user/list')
@token_required
def get_user_list():
	return ''

@app.route('/user/<username>')
def get_user_token():
	username = request.view_args['username']
	if not username:
		return make_response('Unable to fetch user token', 404, {'WWW-Authenticate': 'Basic realm="username required"'})
	try:
		user_file = open('users/' + user, 'rb')
		lines = [line.rstrip() for line in file]
		return jsonify({'token': lines[2]})
	except:
		return make_response('Unable to fetch user token', 404, {'WWW-Authenticate': 'Basic realm="unable to find the user info"'})

# create a user with the user file with the given info
# returns a token for user to store (probably will be in a file too, so it can be reusable)
@app.route('/user/create')
def create_user():
	auth = request.authorization
	password = ''
	if auth:
		username = auth.username
		password = auth.password	
	else:
		return make_response('Create user failed', 403, {'WWW-Authenticate': 'Basic realm="login required"'})
	with open('users/' + user_file_name + '.txt', 'w') as f:
		f.write(username + '\n')
		f.write(password + '\n')
		token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=100)}, app.config['SECRETE_KEY']) 
		f.write(token)
		f.close()

	return jsonify({'token': token})

@app.route('/connect')
def connect_users():
	return ''

def store_file(filename, content):
	with open('users/' + filename + '_filename', 'w') as f:
		try:
			f.write(content)
		except:
			return False
		f.close()
	return True

def encrypt_file(filename):
	return ''

if __name__ == '__main__':
	app.run(debug=True)
	