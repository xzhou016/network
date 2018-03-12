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

#Create 4 sockets
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
#Set all pocket to listen
s1.listen(10)
s2.listen(10)
s3.listen(10)
print 'Socket now listening'


#Generate Bridge Protocol Data Unit
myPriority = '32768:'
myMac = commands.getoutput("/sbin/ifconfig | grep -i \"HWaddr\" | awk '{print $5}'")
BPDU = [myPriority, myMac, myPriority + myMac]
print BPDU
#print 'BPDU as int: '
#print get_mac()

def broadcast(conn):
	



#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	conn.send('Welcome to the forwarder. Type something and hit enter\n')
	#infinite loop so that function do not terminate and thread do not end.
	while True:
		#Receiving from client
		data = conn.recv(1024)
		data = data.split()
		print data
		if data[0] == 'pingmac':
			sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			remote_ip = socket.gethostbyname(arp[1])
			reply = 'arp '
			#conn.sendall(reply)
			sc.connect((remote_ip, arp[4]))
			sc.sendall(reply)			

		if data[0]  == '!q':
			break
	#came out of loop
	conn.close()
	s1.close()
	s2.close()
	s3.close()
	sys.exit()

#now keep talking with the client
while 1:
	#wait to accept a connection - blocking call
	conn, addr = s1.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	#start new thread takes 1st argument as a function name to be run, 
	#second is the tuple of arguments to the function.
	start_new_thread(clientthread ,(conn,))

s1.close()
