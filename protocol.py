import socket
import sys
from thread import *
from sys import argv
 
HOST = 'localhost'   #  available interfaces
print argv
#PORT = int(argv[1]) # my port
SERVER_PORT = 8888
myip = socket.gethostbyaddr(argv[1])
#mymac = argv[2]
#myport= int(argv[3])


#Define a new list
arp = ['10.0.100.3', '08:00:27:58:32:0d', 60, 8001]
arpList = [] 
broadCastList = [8000, 8001, 8002, 8003]

#Create 4 sockets
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created' 
print  (s1 , s2 ,s3 ,s4)  
 
try:
#	s1.bind((myip, arp[3])
#	s.bind((myip, myport)
	s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s1.bind((myip, SERVER_PORT)
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
	
print 'Socket bind complete'

s1.listen(10)
print 'Socket now listening'

#connect to server
sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#remote_ip = socket.gethostbyname(myip)


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
		#param, send_host ,send_port, msg = data.split()
#		if data[0]  == '!fw':
#			#connect to server
#			sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#			remote_ip = socket.gethostbyname(data[1])
#			reply = 'Ok from forwarder...' + data[3] + '\n'
#			conn.sendall(reply)
#			sc.connect((remote_ip, int(data[2])))
#			sc.sendall(data[3]+ '\n')
#			dataList.append(str(HOST))
#i			dataList.append(str(PORT))
#			dataList.append(str(sc.getsockname()))
#			dataList.append(data[3]+ '\n')
#			myList.append(dataList)
#			sc.close()
#		elif data[0]  == '!report':
#			for i in myList:
#				print i	
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
