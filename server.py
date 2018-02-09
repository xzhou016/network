import socket
import sys
from thread import *
 
HOST = 'localhost'   #  available interfaces
PORT = 8888 # my port

#Define a new list
myList = []
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
	s.bind((HOST, PORT))
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
	
print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'


#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
	
	#infinite loop so that function do not terminate and thread do not end.
	while True:
		
		#Receiving from client
		data = conn.recv(1024)
		if data[0:2] == '!q':
			break
		elif data[0:8] == '!sendall':
			#for member in myList:
			print 	#	member.sendall(data[9:1024])
		else:
			reply = 'Received data from forwarder ' + data
			print reply
			break
	#came out of loop
	conn.close()
	#myList.remove(conn)
 
#now keep talking with the client
while 1:
	#wait to accept a connection - blocking call
	#wait to accept a connection - blocking call
	conn, addr = s.accept()
	#myList.append(conn)
	print 'Connected with ' + addr[0] + ':' + str(addr[1])

	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
	start_new_thread(clientthread ,(conn,))

s.close()
