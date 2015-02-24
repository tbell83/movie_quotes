#!/usr/bin/python
import socket
import argparse
import sys
from random import randint
from thread import *

parser = argparse.ArgumentParser()
parser.add_argument('-p', action='store', default='8080', dest='port')
parser.add_argument('-s', action='store', dest='input_file')

args = parser.parse_args()

if args.input_file is None:
    print "Need some quotes"
    sys.exit()

port = int(args.port)
input_file = str(args.input_file)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Binding socket"
server_socket.bind((socket.gethostname(), port))
server_socket.listen(5)
print "Listening on port: " + str(port)


def get_quote():
    fo = open(input_file, 'r')
    quotes = fo.read().split('\n\n')
    return str(quotes[randint(0, len(quotes))]) + "\n"


def clientthread(conn):
    conn.send(get_quote())
    conn.close()

while 1:
    (clientsocket, address) = server_socket.accept()
    print 'Connected to ' + address[0] + ':' + str(address[1])
    start_new_thread(clientthread, (clientsocket,))

server_socket.close()
