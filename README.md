# Multi-Switch Flow Table Analyzer
**Name:** Catherine D  
**SRN:** PES1UG24CS120

## Problem Statement
Design and implement an SDN-based flow table analyzer that monitors and displays flow rule usage across multiple OpenFlow switches in a Mininet topology using a POX controller.

## Project Structure
- `topology.py` - Mininet topology with 3 switches and 6 hosts
- `flow_analyzer_controller.py` - POX SDN controller with OpenFlow flow rules
- `analyzer.py` - Flow table analyzer that queries and displays rule usage

## Setup Requirements
- Mininet 2.3.0
- POX Controller (gar branch)
- Open vSwitch 3.3.4
- Python 3.x

## Execution Steps

### Step 1 - Start POX Controller (Terminal 1)
cd ~/pox
python3 pox.py log.level --DEBUG controller

### Step 2 - Start Mininet Topology (Terminal 2)
cd ~/sdn_project
sudo python3 topology.py

### Step 3 - Run Flow Analyzer (Terminal 3)
cd ~/sdn_project
sudo python3 analyzer.py --interval 5 --rounds 5

## Topology
h1, h2 -- s1 -- s2 -- s3 -- h5, h6
                |
              h3, h4

## Flow Rules Installed per switch
Priority 100 - ARP - FLOOD
Priority 90  - ICMP - FLOOD
Priority 80  - TCP - FLOOD
Priority 70  - UDP - FLOOD
Priority 10  - DEFAULT - FLOOD

## Test Scenarios

### Scenario 1 - Normal Connectivity
mininet> pingall
Results: 0% dropped (30/30 received)

### Scenario 2 - TCP Traffic via iperf
mininet> iperf h1 h6
TCP rule becomes ACTIVE with high packet counts.

### Scenario 3 - Link Failure and Recovery
mininet> link s1 s2 down
mininet> pingall
Results: 53% dropped (14/30 received)

mininet> link s1 s2 up
mininet> pingall
Results: 0% dropped (30/30 received)

## Expected Output
- Flow table displayed per switch with Rule#, Priority, Packets, Bytes, Type, Status
- ACTIVE rules marked with >>
- UNUSED rules clearly labeled
- Summary showing total switches, rules, packets, active and unused counts

## Tools Used
- Mininet - network emulation
- POX - SDN controller
- Open vSwitch - software switch
- tcpdump - packet capture and validation

## References
- Mininet Documentation: http://mininet.org
- POX Controller: https://github.com/noxrepo/pox
- OpenFlow 1.0 Specification: https://opennetworking.org
- Open vSwitch: https://www.openvswitch.org
