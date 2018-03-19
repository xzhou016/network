from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class Bridges(Topo):
	def __init__(self):
		"Create custom topo."
		#Init topo
		Topo.__init__(self)
		#Add hosts and switches
		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		h3 = self.addHost('h3')
		h4 = self.addHost('h4')
		switch = self.addSwitch('s1')
		#Add links
		self.addLink(h1, switch)
		self.addLink(h2, switch)
		self.addLink(switch, h3)
		self.addLink(switch, h4)

topos = {'bridges': (lambda: Bridges())}
