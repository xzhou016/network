import socket, optparse
import commands

parser = optparse.OptionParser()
parser.add_option('-i', dest='ip', default='10.0.0.2')
parser.add_option('-p', dest='port', type='int', default=8000)
parser.add_option('-m', dest='msg')
(options, args) = parser.parse_args()

def myBPDU():
	#Generate Bridge Protocol Data Unit
	myPriority = '32768:'
	myMac = commands.getoutput("/sbin/ifconfig | grep -i \"HWaddr\" | awk '{print $5}'")
	BPDU = [myPriority, myMac, myPriority + myMac]
	return BPDU[2]
	#print 'BPDU as int: '
	#print get_mac()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print 'Sending: ', myBPDU()
s.sendto(myBPDU(), (options.ip, options.port) )
