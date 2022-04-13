import socket
import struct
import threading
from EXPO import *

#TODO:          error handling
#               client/server authentication?
#               client->client handshake & authentication

def connect(client, HOST, PORT):
    client.connect((HOST, PORT))
    send(client, input('enter your username:').encode())
    response = recieve(client)
    if response != b'okay':
        return
    dest = input('connection made, who do you want to message?')
    chat(client, dest)
    
def chat(client, dest):
    print('from now on, just type message and hit enter to send!')
    recv_t = threading.Thread(target = recv_chat, args = (client,))
    recv_t.start()
    send_chat(client, dest)

def send_chat(client, dest):
    while(True):
        msg = input('you: ')
        msg = dest + '\n\n' + msg
        send(client, msg.encode())

def recv_chat(client):
    while(True):
        msg = recieve(client).decode()
        print(msg)


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
    PORT = 9996
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect(client, HOST, PORT)
    client.close()
