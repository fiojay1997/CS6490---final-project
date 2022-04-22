import secrets
from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

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

@app.route('/user', method=['GET'])
def get_user_list():
	return ''

@app.route('/user/<id>', method=['GET'])
def get_user_token():
	return ''

@app.route('/user', method=['POST'])
def create_user():
	return ''

@app.route('/connect', method=['POST'])
def connect_users():
	return ''

if __name__ == '__main__':
	app.run(debug=True)
	