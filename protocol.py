import socket
import sys
from thread import *
from sys import argv
import commands
from uuid import getnode as get_mac
 
HOST = argv[1]   #  available interfaces
ips = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | awk '{print $2}'")
print ips
#PORT = int(argv[1]) # my port
SERVER_PORT = 8888
#myip = socket.gethostbyaddr(argv[1])
#print myip
#mymac = argv[2]
#myport= int(argv[3])


#Define a new list
portList = [1, 2, 3]

#Create 3 sockets
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print 'Socket created' 
print  (s1 , s2 ,s3 )

#Bind all sockets
try:
	s1.bind((HOST, portList[0]))
	s2.bind((HOST, portList[1]))
	s3.bind((HOST, portList[2]))
	s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	s3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
except socket.error, msg:
	print 'Bind failed. Error code: ' + str(msg[0]) + '\nMessage: ' + msg[1]
	sys.exit()
print 'Socket bind complete' 

#TODO:
# Count down for sockstream 
# Put each in a thread

#Generate Bridge Protocol Data Unit
myPriority = '32768:'
myMac = commands.getoutput("/sbin/ifconfig | grep -i \"HWaddr\" | awk '{print $5}'")
BPDU = [myPriority, myMac, myPriority + myMac]
print BPDU
#print 'BPDU as int: '
#print get_mac()

#Set all pocket to listen
#s1.listen(10)
#s2.listen(10)
#s3.listen(10)
def listenport(s):
	s.listen(10)
	print 'Socket now listening'
	
def decode(msg):
	msg_array = msg.split(':')
	priority = msg.pop(0)
	for i in msg:
		mac += i
	if 

def clientthread(rconn):
	print 'Client created'
	while True:
		rconn.sendall('BPDU')
		response = conn.recv(2048)
	rconn.close()

start_new_thread(listenport,(s1,))

while 1:
	
	conn, addr = s1.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	start_new_thread(clientthread ,(conn,))
