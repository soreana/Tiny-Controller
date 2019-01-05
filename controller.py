#!/usr/bin/python

import socket
import threading
import sys
from time import sleep

# if false disable debug lines
debug = False

if len(sys.argv) >= 2 and sys.argv[1] == "debug":
    print "entering debug mode."
    debug = True

# set up server
s = socket.socket()
host = '0.0.0.0'
port = 8000
s.bind((host, port))

s.listen(5)  # up to 5 concurrent connections


def parse_of_header( s ):
    if len(s) < 8:
        return 8

    length = (ord(s[3]) + ord(s[2])*2**8)

    if debug:
        print ( "version: %s" % ord(s[0]) )
        print ( "type: %s" % ord(s[1]) )
        print ( "length: %s" % length )
        print ( "xid: %s" % (ord(s[7]) + ord(s[6])*2**8 + ord(s[5])*2**16 + ord(s[4])*2**24 ))
    return length
    
def read_of_header(c):
    cur = c.recv(8)
    return parse_of_header(cur) - 8, cur


def responde_to_mininet_connection(s):
    c,addr = s.accept()  # Establish connection with socket.
    if debug:
        print 'Got mininet test packet.'
    c.close()

responde_to_mininet_connection(s)

while True:

    c, addr = s.accept()  # Establish connection with socket.
    if debug:
        print 'Got connection from', addr
    #sleep(5)
    payload_size , cur = read_of_header(c)
    print (payload_size)
    c.send(cur)
