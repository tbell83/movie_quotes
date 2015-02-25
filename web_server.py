#!/usr/bin/python
import socket
import argparse
import sys
import urllib2
from random import randint
from thread import *

parser = argparse.ArgumentParser()
parser.add_argument('-p', action='store', default='8080', dest='port')
parser.add_argument('-s', action='store', dest='input_file')

args = parser.parse_args()

movies = None
quotes = None

if args.input_file is None:
    response = urllib2.urlopen('http://www.coverfire.com/files/quotes.txt')
    data = response.read()
    quotes = data.split("\n\n")
else:
    input_file = str(args.input_file)
    fo = open(input_file, 'r')
    movies = fo.read().split('\n\n\n');

port = int(args.port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), port))
server_socket.listen(5)
print "Listening on port: " + str(port)


def get_quote():
    if movies is not None:
        movie = movies[randint(0,len(movies))].split("\n\n")
        credit = movie[0].split("\n")[0]
        temp = movie[0].split("\n")
        temp.pop(0)
        temp2 = ""
        for item in temp:
            temp2 = temp2 + item + "\n" 
        movie[0] = temp2
        quote = movie[randint(0,len(movie))]
    elif quotes is not None:
        quote = quotes[randint(0,len(quotes))]
        quote = quote.split("\t-- ")
        if len(quote) > 1:
            for i in range(1,len(quote)):
                credit = quote[i].rstrip("\n")
        quote = quote[0]
    else:
        quote = "Something has gone terribly, terribly wrong."
        credit = "Uh oh..."
    output = "<h1>" + credit + "</h1>" + "<br/>"  + quote.replace("\n", "<br/>")
    return output


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
