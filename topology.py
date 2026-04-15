# Name: Catherine D
# SRN: PES1UG24CS120
# Project: Multi-Switch Flow Table Analyzer
# Description: Custom Mininet topology with 3 switches and 6 hosts

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def create_topology():
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)

    info("*** Adding Remote Controller (POX)\n")
    c0 = net.addController('c0', controller=RemoteController,
                            ip='127.0.0.1', port=6633)

    info("*** Adding Switches\n")
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    info("*** Adding Hosts\n")
    # 2 hosts per switch
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')
    h5 = net.addHost('h5', ip='10.0.0.5/24')
    h6 = net.addHost('h6', ip='10.0.0.6/24')

    info("*** Creating Links\n")
    # Hosts to switches
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(h5, s3)
    net.addLink(h6, s3)

    # Switch to switch (linear chain)
    net.addLink(s1, s2)
    net.addLink(s2, s3)

    info("*** Starting Network\n")
    net.start()

    info("*** Network is ready!\n")
    info("*** Topology: h1,h2 -- s1 -- s2 -- s3 -- h5,h6\n")
    info("***                          |              \n")
    info("***                        h3,h4            \n")

    info("*** Running CLI (type 'exit' to quit)\n")
    CLI(net)

    info("*** Stopping Network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_topology()
