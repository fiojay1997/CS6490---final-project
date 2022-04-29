import socket
import struct
import base64
import hmac
import hashlib
import threading
from EXPO import *
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#TODO:          error handling
#               client/server authentication?
#               client->client handshake & authentication
p = 784313
g = 1907
secret_key = ''
preshared_secret = b'7jay7leo7stev7'
user = ''
recv_hash = ''

def connect(client, HOST, PORT):
    client.connect((HOST, PORT))
    global user
    user = input('enter your username: ')
    send(client, user.encode())
    response = recieve(client)
    if response != b'okay':
        return
    dest = input('connection made, who do you want to message? ')
    chat(client, dest)
    
def chat(client, dest):
    s_a = int(input('enter a number at least 5 digits long: '))
    recv_t = threading.Thread(target = recv_chat, args = (client, dest, s_a))
    recv_t.start()
    send_chat(client, dest, s_a)

def send_chat(client, dest, s_a):
    #formulate t_a, send t_a
    dest = dest.encode()
    t_a = str(exponentiate(g, s_a, p))
    msg = dest + b'\n\n' + t_a.encode()
    send(client, msg)

    global secret_key
    while(secret_key == ''):
        continue
    crypt = get_key()
    
    global user
    my_hash = get_hmac(user.encode())
    expected_hash = get_hmac(dest)

    msg = dest + b'\n\n' + my_hash
    send(client, msg)

    global recv_hash
    while(recv_hash == ''):
        continue

    print('expected:', expected_hash)
    print('recieved:', recv_hash)

    if recv_hash != expected_hash:
        print('error')
        raise RuntimeError('mismatched hash!')

    print('from now on, just type message and hit enter to send!')
    while(True):
        msg = input('you: ')
        msg = dest + b'\n\n' + crypt.encrypt(msg.encode())
        send(client, msg)

def recv_chat(client, dest, s_a):
    #reeive t_b, formulate key (exponentiate(t_b, s_a, p))
    msg = recieve(client).decode()
    msg = msg.split(' ')
    t_b = int(msg[1])
    global secret_key 
    secret_key = exponentiate(t_b, s_a, p)
    crypt = get_key()

    msg = recieve(client)
    msg = msg.split(b' ')
    r_h = msg[1]

    global recv_hash
    recv_hash = r_h

    dest = dest + ': '
    dest = dest.encode()
    while(True):
        msg = recieve(client)
        msg = msg.replace(dest, b'')
        msg = bytes(msg)
        msg = crypt.decrypt(msg)
        print("\n"+ (dest + msg).decode())


def get_key():
    global secret_key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'\xa1\xb2\xc3\xd4\xe5\xf6\x07\x88',
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret_key.to_bytes(8, 'little')))
    f = Fernet(key)
    return f

def get_hmac(source):
    s = preshared_secret + source
    hash = hmac.new(s, secret_key.to_bytes(8, 'little'), hashlib.sha256)
    return hash.digest()

#       https://docs.python.org/3.6/howto/sockets.html#using-a-socket
#       https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
#
# helper methods to send and recieve entire message given a socket (and message)

def send(sock, msg):
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recieve(sock):
    msg_len = receive_all(sock, 4)
    if not msg_len:
        raise RuntimeError("socket connection broken")
    msg_len = struct.unpack('>I', msg_len)[0]
    # Read the message data
    return receive_all(sock, msg_len)


def receive_all(sock, size):
    msg = bytearray()
    received = 0
    while received < size:
        packet = sock.recv(size - received)
        if packet == b'':
            raise RuntimeError("socket connection broken")
        msg.extend(packet)
        received += len(packet)
    return msg


if __name__ == '__main__':
    #alice
    HOST = '127.0.0.1'
    PORT = 9999
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect(client, HOST, PORT)
    client.close()