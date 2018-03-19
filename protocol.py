import socket
import sys
import threading
from thread import *
from sys import argv
import commands
from uuid import getnode as get_mac
import copy

ips = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | awk '{print substr($2,6)}'| head -1")
#print ips

#Define a new list
ipList = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4']
portList = [1, 2, 3]
portCostList = []
status = []
statusList = []
dataList = []
addrList = []
macList = []

#Define mininum distant for port
min_dist = float('Inf')
count_broadcast = 5
count_recv = 10

#Create 4 sockets
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print 'Socket created' 
#print  (s1 , s2 ,s3 )

#Bind all sockets
try:
	s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	s3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	s1.bind((ips, portList[0]))
	s2.bind((ips, portList[1]))
	s3.bind((ips, portList[2]))
except socket.error, msg:
	print 'Bind failed. Error code: ' + str(msg[0]) + '\nMessage: ' + msg[1]
	sys.exit()
print 'Socket bind complete' 

def myBPDU():
	#Generate Bridge Protocol Data Unit
	myPriority = '32768'
	myMac = commands.getoutput("/sbin/ifconfig | grep -i \"HWaddr\" | awk '{print $5}'")
	iMac = get_mac()
	BPDU = myPriority + ',' + str(iMac) + ',' + myMac
	return BPDU

def create_port_table():
	for i in portList:
		status.append('')
		status.append(i)
		status.append('RP')
	#print status

	
#broadcast and receive threads
def broadcast_timer():
	global count_broadcast
	global count_recv
	if count_broadcast:
		threading.Timer(5.0,broadcast_timer).start()
		broadcast()
		count_broadcast = count_broadcast - 1
		count_recv = count_recv - 1
		
def receive_timer():
	global count_broadcast
	global count_recv
	if count_broadcast:
		threading.Timer(2.0,receive_timer).start()
		receive()
	elif count_recv <= 5:
		
		cost = elect_root()
		#print 'lowest cost mac: ' , cost
		set_mac(cost)
		count_recv = count_recv - 1

def broadcast():
	#remove self
	#print ipList
	if ips in ipList:
		ipList.remove(ips)
	#send out BPDU to all ports
	for ip in ipList:
		for port in portList:
			#print 'sending to:', ip, port
			s1.sendto(myBPDU(), (ip, port))
			s2.sendto(myBPDU(), (ip, port))
			s3.sendto(myBPDU(), (ip, port)) 

def populate_data_addr():
	dataList.append(myBPDU())
	for port in portList:
		addrList.append((ips, port))
	#print dataList, addrList

def receive():
	#get messege from port 1
	data , addr= s1.recvfrom(1024)
	if data not in dataList:
		dataList.append(data)
	if addr not in addrList:
		addrList.append(addr)
	
	#get messege from port 2
	data , addr= s2.recvfrom(1024)
	if data not in dataList:
		dataList.append(data)
	if addr not in addrList:
		addrList.append(addr)
	
	#get messege from port 3
	data , addr= s3.recvfrom(1024)
	if data not in dataList:
		dataList.append(data)
	if addr not in addrList:
		addrList.append(addr)
	print "Received: ", dataList, addrList
	
	
def elect_root():
	for data in dataList:
		data = data.split(',')
		macList.append(data)
	#print macList
		
	for mac in macList:
		cost = float(mac[0]) * float(mac[1])
		if cost not in portCostList:
			portCostList.append(cost)
	#print portCostList
	return portCostList.index(min(portCostList))


def set_mac(addr):
	for i in portList:
		if status:
			del status[:]
		status.append(macList[addr][2])
		status.append(i)
		status.append('DP')
		statusList.append(copy.copy(status))
		del addrList[addr]
	del macList[addr]
	print addrList
	
	for mac in macList:
		if status:
			del status[:]
		status.append(mac[2])
		status.append(addrList[addr][1])
		status.append('RP')
		statusList.append(copy.copy(status))
		del addrList[addr]
		
	for addr in addrList:
		if status:
			del status[:]
		status.append(mac[2])
		status.append(addr[1])
		status.append('BP')
		statusList.append(copy.copy(status))
	
	#print dataList
	print statusList
		

	
#create_port_table()
populate_data_addr()
broadcast_timer() #broadcast self on all ports
receive_timer() #finish grabing all forward messege



#populate_bridge_table()

