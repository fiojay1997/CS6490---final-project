import tweepy
import base64
import threading
from EXPO import *
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

p = 784313
g = 1907
secret_key = ''
destination = ''
steven = 'stev_thomson'
jay = 'JayFuKJ'
send_init = False


def set_up_connection(user):
    global destination
    if user == 'steven':
        destination = jay
    else if user == 'jay':
        destination = steven

    consumer_key, consumer_secret, access_token, secret_token = get_auth_and_tokens(user)
    api = config_connection(consumer_key, consumer_secret, access_token, secret_token)
    return api


def get_auth_and_tokens(user):
    file = open('{}.txt'.format(user), 'r')
    consumer_key = file.readline()
    consumer_secret = file.readline()
    access_token = file.readline()
    secret_token = file.readline()
    return consumer_key, consumer_secret, access_token, secret_token


def config_connection(consumer_key, consumer_secret, access_token, secret_token):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, secret_token)
    api = tweepy.API(auth)
    return api


def begin_secure_chat(api):
    s_a = int(input('enter a number at least 5 digits long: '))
    recv_t = threading.Thread(target = recv_chat, args = (api, s_a))
    recv_t.start()
    send_chat(api, s_a)


def send_chat(api, s_a):
    t_a = str(exponentiate(g, s_a, p))
    send(api, t_a)

    global send_init = True
    
    global secret_key
    while(secret_key == ''):
        continue

    crypt = get_crypto_suite()
    print('from now on, just type message and hit enter to send!')

    while(True):
        msg = input('you: ')
        send(api, crypt.encrypt(msg.encode()).decode())
    

def recv_chat(api, s_a):
    global secret_key
    global send_init
    global destination

    while(not send_init):
        continue

    dest_id = api.get_user(destination)

    received_msgs = []
    messages = api.list_direct_messages(count=5)
    for message in reversed(messages):
        sender_id = message.message_create["sender_id"]
        text = message.message_create["message_data"]["text"]
        if sender_id == dest_id and text.isnumeric():
            received_msgs.append(text)
            t_b = int(text)
            secret_key = exponentiate(t_b, s_a, p)
            break

    crypt = get_key()
    
    while(True):
        messages = api.list_direct_messages(count=5)
        for message in messages:
            sender_id = message.message_create["sender_id"]
            if sender_id == dest_id:
                text = message.message_create["message_data"]["text"]
                msg = crypt.decrypt(text.encode())
                if msg not in received_msgs:
                    received_msgs.append(msg)
                    msg = destination + ': ' + msg
                    print(msg)

    

def send(api, msg):
    global destination

    user = api.get_user(destination)
    recipient_id = user.id_str
    api.send_direct_message(recipient_id, msg)


def get_crypto_suite():
    global secret_key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'\xa1\x2b\xc3\x4d\xe5\x6f\x07\x88',
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret_key.to_bytes(8, 'little')))
    f = Fernet(key)
    return f


if __name__ == '__main__':
    user = input('enter username: (steven OR jay')
    api = set_up_connection(user)
    begin_secure_chat(api)
