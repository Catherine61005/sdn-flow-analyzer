# Name: Catherine D
# SRN: PES1UG24CS120
# Project: Multi-Switch Flow Table Analyzer
# Description: Queries and displays flow table statistics from all switches

import subprocess
import time
import os

def clear_screen():
    os.system('clear')

def get_switches():
    """Get list of active OVS switches"""
    result = subprocess.run(['sudo', 'ovs-vsctl', 'list-br'],
                          capture_output=True, text=True)
    switches = result.stdout.strip().split('\n')
    return [s for s in switches if s]

def get_flow_stats(switch):
    """Get flow table from a specific switch"""
    result = subprocess.run(['sudo', 'ovs-ofctl', 'dump-flows', switch],
                          capture_output=True, text=True)
    return result.stdout

def parse_flows(raw_output):
    """Parse raw flow output into readable format"""
    flows = []
    for line in raw_output.strip().split('\n'):
        if 'actions' not in line:
            continue

        flow = {}

        # get priority
        if 'priority=' in line:
            try:
                flow['priority'] = line.split('priority=')[1].split(',')[0].split(' ')[0]
            except:
                flow['priority'] = 'N/A'
        else:
            flow['priority'] = '0'

        # get packet count
        if 'n_packets=' in line:
            try:
                flow['packets'] = line.split('n_packets=')[1].split(',')[0]
            except:
                flow['packets'] = '0'
        else:
            flow['packets'] = '0'

        # get byte count
        if 'n_bytes=' in line:
            try:
                flow['bytes'] = line.split('n_bytes=')[1].split(',')[0]
            except:
                flow['bytes'] = '0'
        else:
            flow['bytes'] = '0'

        # get action
        if 'actions=' in line:
            try:
                flow['action'] = line.split('actions=')[1].strip()
            except:
                flow['action'] = 'N/A'
        else:
            flow['action'] = 'N/A'

        # figure out rule type
        if 'arp' in line.lower():
            flow['type'] = 'ARP'
        elif 'icmp' in line.lower():
            flow['type'] = 'ICMP'
        elif 'tcp' in line.lower():
            flow['type'] = 'TCP'
        elif 'udp' in line.lower():
            flow['type'] = 'UDP'
        else:
            flow['type'] = 'DEFAULT'

        flows.append(flow)
    return flows

def display_analysis(switches_data):
    """Display formatted flow table analysis"""
    clear_screen()
    print("=" * 65)
    print("       MULTI-SWITCH FLOW TABLE ANALYZER")
    print("=" * 65)
    print("Time:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print()

    total_flows = 0
    total_packets = 0

    for switch, flows in switches_data.items():
        print("-" * 65)
        print("  Switch: %s  |  Total Rules: %d" % (switch, len(flows)))
        print("-" * 65)
        print("  %-8s %-10s %-12s %-12s %-10s" %
              ("Rule#", "Priority", "Packets", "Bytes", "Type"))
        print("  " + "-" * 55)

        for i, flow in enumerate(flows):
            packets = int(flow['packets']) if flow['packets'].isdigit() else 0
            total_packets += packets

            # highlight active rules
            marker = " >>" if packets > 0 else "   "
            print("%s%-5s %-10s %-12s %-12s %-10s" % (
                marker,
                str(i+1),
                flow['priority'],
                flow['packets'],
                flow['bytes'],
                flow['type']
            ))
        total_flows += len(flows)
        print()

    print("=" * 65)
    print("  SUMMARY")
    print("  Total Switches  : %d" % len(switches_data))
    print("  Total Rules     : %d" % total_flows)
    print("  Total Packets   : %d" % total_packets)
    print("  Active Rules(>0): %d" % sum(
        1 for flows in switches_data.values()
        for f in flows if f['packets'].isdigit() and int(f['packets']) > 0
    ))
    print("=" * 65)

def run_analyzer(interval=5, rounds=5):
    """Main analyzer loop"""
    print("Starting Flow Table Analyzer...")
    print("Querying every %d seconds for %d rounds" % (interval, rounds))
    time.sleep(2)

    for round_num in range(1, rounds+1):
        switches = get_switches()
        if not switches:
            print("No switches found! Is Mininet running?")
            time.sleep(interval)
            continue

        switches_data = {}
        for switch in switches:
            raw = get_flow_stats(switch)
            flows = parse_flows(raw)
            switches_data[switch] = flows

        display_analysis(switches_data)
        print("\n  Round %d/%d complete. Refreshing in %ds..." % 
              (round_num, rounds, interval))
        time.sleep(interval)

    print("\nAnalysis complete!")

if __name__ == '__main__':
    run_analyzer(interval=5, rounds=5)
