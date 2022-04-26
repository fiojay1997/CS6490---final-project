import socket
import struct
import threading

#TODO:          error handling
#               client/server authentication

clients = []

def main():
    IP = '0.0.0.0'
    PORT = 9999
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)

    print('Waiting for clients to connect on PORT ', PORT)

    while(True):
        #loop for multiple connections
        client, addr = server.accept()
        print('Connection to server made!')
        client_handler = threading.Thread(target = handle_client, args = (client,addr,))
        client_handler.start()


def handle_client(client_socket, addr):
    username = recieve(client_socket).decode()
    clients.append({'sock':client_socket, 'addr':addr, 'user':username})
    ok_msg = b'okay'
    send(client_socket, ok_msg)

    #TODO: error handling
    while(True):
        msg = recieve(client_socket)
        dest, msg = split_msg(msg.decode())
        forward_msg(username, dest, msg)


def split_msg(msg):
    msg = msg.split('\n\n')
    return msg[0], msg[1].encode()


def forward_msg(source, dest, msg):
    forward_msg = source.encode() + b': ' + msg

    for client in clients:
        if client['user'] == dest:
            send(client['sock'], forward_msg)
            return

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
    #bob
    main()