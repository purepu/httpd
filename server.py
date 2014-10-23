import socket
import sys
import os
from os import listdir, path

HOST = '127.0.0.1'
PORT = 8080 
BACKLOG = 10
PATH = '.' 

list_file = [f for f in listdir(PATH) if path.isfile(f)]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "ok"
try:
    s.bind((HOST, PORT))
except socket.error as message:
    print "Failed due to %s" %message
    sys.exit

s.listen(BACKLOG)
print "connected"


while 1:
    client, addr = s.accept()
    header_dic = {}
    data = client.recv(1024)
    print data
    data = data.split()
    print data
    for i in range(3, len(data)):
        if data[i][-1] == ':':
            header_dic[data[i]] = []
            j = i
        else:
            header_dic[data[j]].append(data[i])
    print header_dic
    url = data[1]
    if url == '/':
        url = ''
    else:
        url = data[1][1:]
    print url
    if not url:
        client.send('HTTP/1.0 200 OK\nContent-Type: text/html\n\n')
        f = open('index.html')
    else:
        if url in list_file:
            client.send('HTTP/1.0 200 OK\nContent-Type: text/html\n\n')
            f = open(url)
        else: 
            client.send('HTTP/1.0 404 Not Found\nContent-Type: text/html\n\n')
            f = open('not_found.html')
    client.send(f.read())
    client.close()
