import socket
import sys

HOST = '127.0.0.1'
PORT = 8080 
BACKLOG = 10

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
    data = client.recv(1024)
    data = data.split()
    print data
    for i in range(0, 10):
        print data[i]
    if data[0] == "GET":
        client.send("200 OK")
        client.send("hello fish")
    else:
        client.send("400 not found")
    client.close()



    
