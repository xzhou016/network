# CS 164 Spanning Tree Protocol Network Project
## Runnable
* To run the code first create a mininet topology by typing "sudo mn --custom bridges.py --topo bridges"
* When mininet has setup the topology, type "xterm h1 h2 h3 h4", this will launch 4 xterm windows
* Within each window type "python protocol.py", it will sent out broadcast message and return a table consist of mac address of each host, port number and the status of the port
