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
    print "Need some quotes!"
    sys.exit()

port = int(args.port)
input_file = str(args.input_file)

print "Loading quotes:"
fo = open(input_file, 'r')
movies = fo.read().split('\n\n\n');

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), port))
server_socket.listen(5)
print "Listening on port: " + str(port)


def get_quote():
    movie = movies[randint(0,len(movies))].split("\n\n")
    movie_name = movie[0].split("\n")[0]
    temp = movie[0].split("\n")
    temp.pop(0)
    temp2 = ""
    for item in temp:
        temp2 = temp2 + item + "\n" 
    movie[0] = temp2
    quote = movie[randint(0,len(movie))]
    return movie_name + "<br/>"  + quote.replace("\n", "<br/>")


def clientthread(conn):
    try:
        quote = get_quote()
    except:
        quote = "Things have gone wrong"

    html = "<html>\n  <body>\n    <p>{0}</p>\n  </body>\n</html>".format(quote)

    conn.send(html)
    conn.close()

while 1:
    (clientsocket, address) = server_socket.accept()
    print 'Connected to ' + address[0] + ':' + str(address[1])
    start_new_thread(clientthread ,(clientsocket,))

server_socket.close()
