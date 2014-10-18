import socket, sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("www.google.com", 80))
s.send("GET / HTTP/1.0\n\n")

#f = open("google.html", "r+")

while 1:
    buf = s.recv(1000)
    if not buf:
        break
    sys.stdout.write(buf)
    #f.write(buf)
#f.close()
s.close
