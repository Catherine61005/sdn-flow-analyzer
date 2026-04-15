# Multi-Switch Flow Table Analyzer
**Name:** Catherine D
**SRN:** PES1UG24CS120
**Course:** UE24CS252B - Computer Networks

---

## Problem Statement
Implement an SDN-based solution using Mininet and POX controller that analyzes 
flow tables across multiple switches and displays rule usage statistics.

---

## Topology
h1, h2 -- s1 -- s2 -- s3 -- h5, h6
                 |
               h3, h4

- 3 OpenFlow switches (s1, s2, s3)
- 6 hosts (h1-h6)
- POX SDN Controller

---

## Files
| File | Description |
|------|-------------|
| flow_analyzer_controller.py | POX controller with flow rule installation |
| topology.py | Mininet custom topology |
| analyzer.py | Flow table analyzer and display script |

---

## Setup & Execution

### Step 1: Start POX Controller
cd ~/pox
python3 pox.py log.level --DEBUG flow_analyzer_controller

### Step 2: Start Mininet Topology (new terminal)
cd ~/sdn_project
sudo python3 topology.py

### Step 3: Run tests inside Mininet
pingall
h1 ping -c 4 h6
h6 iperf -s &
h1 iperf -c 10.0.0.6 -t 5

### Step 4: Run Flow Analyzer (new terminal)
cd ~/sdn_project
sudo python3 analyzer.py

---

## Expected Output
- pingall: 0% packet loss across all 6 hosts
- ping h1 to h6: ~1.5ms average latency across 3 switches
- iperf: ~53 Gbits/sec TCP bandwidth
- Flow Analyzer shows 4 rules per switch, all active

---

## Test Scenarios
### Scenario 1: Full mesh connectivity (pingall)
All 6 hosts across 3 switches ping each other successfully with 0% packet loss.

### Scenario 2: Cross-switch latency (h1 ping h6)
Traffic travels across all 3 switches with minimal latency (~1.5ms average).

### Scenario 3: TCP Throughput (iperf h1 to h6)
TCP bandwidth measured at ~53 Gbits/sec demonstrating high performance SDN forwarding.

---

## Flow Rules Installed (per switch)
| Priority | Type    | Action | Description          |
|----------|---------|--------|----------------------|
| 100      | ARP     | FLOOD  | Handle ARP requests  |
| 90       | ICMP    | FLOOD  | Handle ping traffic  |
| 80       | TCP     | FLOOD  | Handle TCP traffic   |
| 10       | DEFAULT | FLOOD  | Handle all else      |

---

## References
1. Mininet: http://mininet.org
2. POX Controller: https://github.com/noxrepo/pox
3. OpenFlow 1.0 Spec: https://opennetworking.org
