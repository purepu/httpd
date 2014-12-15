import socket
import sys
import os
import random

HOST = '0.0.0.0'
PORT = 8080 
BACKLOG = 10
PATH = '.' 
BUFFERSIZE = 1024

def list_files(path):
    file_list = []
    for dirname, dirnames, filenames in os.walk(path):
        if '.git' in dirnames:
            dirnames.remove('.git')
        for filename in filenames:
            file_list.append(os.path.join(dirname, filename))
    return file_list

def create_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "ok"
    try:
        s.bind((host, port))
    except socket.error as message:
        print "Failed due to %s" %message
        sys.exit()
    return s

def parse_request_header(raw_request):
    lines = raw_request.split('\n')
    hdrs= {}
    for l in lines[1:]:
        cln = l.find(':')
        hdrs[l[:cln]] = l[cln+1:]
    return hdrs

def parse_request_line(raw_request):
    line = raw_request.split('\n')[0]
    return line.split()

if __name__ == '__main__':
    s = create_socket(HOST, PORT)

    s.listen(BACKLOG)
    print "connected"

    while True:
        client, addr = s.accept()
        raw_request = client.recv(BUFFERSIZE)
        print raw_request
        if not raw_request:
            client.send("HTTP/1.0 404 Not Found")
            continue
        method, url, version = parse_request_line(raw_request)
        hdrs = parse_request_header(raw_request)
        cookie = hdrs.get('Cookie')
        if not cookie:
            cookie = random.randint(-100000, 100000) 
            set_cookie = 'Set-Cookie: test=%d;expires=Thu, 01-Jan-2015 00:00:00 GMT' %cookie 
        else:
            set_cookie = ''
        path = '%s%s' % (PATH, url)
        if os.path.isdir(path):
            path = '%s/index.html' % path
        if os.path.exists(path):
            f = open(path)
            #client.send("HTTP/1.0 200 OK\nContent-Type: text/html%s\n\n%s" % (set_cookie, f.read()))
            resp = '\n'.join(('HTTP/1.0 200 OK',
                              'Content-Type: text/html',
                              set_cookie,
                              '\n',
                              f.read()))
            client.send(resp)
        else:
            client.send("HTTP/1.0 404 Not Found")
        client.close()
