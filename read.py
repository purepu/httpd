import socket, sys

'''s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
s.close'''

class SimpleClient:
    
    def __init__(self, server, port = 80):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server, port))
        self.file = self.sock.makefile("rb")

    def send_request(self, request):
        self.sock.send(request + "\r\n\r\n")

    def receive_readline(self):
        s = self.file.readline()
        if not s:
            raise EOFError("end")
        elif s[-2:] == '\r\n':
            s = s[:-2]
        elif s[-1:] == '\n':
            s = s[:-1]
        return s

    def receive_read(self, maxread = None):
        if not maxread:
            return self.file.read()
        else:
            return self.file.read(maxread)

def get(server, port = 80, doc = "/"):
    http = SimpleClient(server, port)
    request = "GET %s  HTTP/1.0 \n\n" %doc
    http.send_request(request)
    while 1:
        s = http.receive_readline()
        if not s:
            break

    return http.receive_read()
        
if __name__ == "__main__":
    data = get("www.google.com")
    f = open("google.html", "r+")
    f.write(data)
    f.close()
    sys.stdout.write(data)
        
        

