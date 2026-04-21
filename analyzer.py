# Name: Catherine D
# SRN: PES1UG24CS120
# Project: Multi-Switch Flow Table Analyzer
# Description: Queries and displays flow table statistics from all switches

import subprocess
import time
import os
import argparse

def clear_screen():
    os.system('clear')

def get_switches():
    result = subprocess.run(['sudo', 'ovs-vsctl', 'list-br'],
                          capture_output=True, text=True)
    switches = result.stdout.strip().split('\n')
    return [s for s in switches if s]

def get_flow_stats(switch):
    result = subprocess.run(['sudo', 'ovs-ofctl', 'dump-flows', switch],
                          capture_output=True, text=True)
    return result.stdout

def extract_field(line, key, default='N/A'):
    try:
        return line.split(f'{key}=')[1].split(',')[0].split(' ')[0]
    except IndexError:
        return default

def parse_flows(raw_output):
    flows = []
    for line in raw_output.strip().split('\n'):
        if 'actions' not in line:
            continue
        flow = {}
        flow['priority'] = extract_field(line, 'priority', default='0')
        flow['packets']  = extract_field(line, 'n_packets', default='0')
        flow['bytes']    = extract_field(line, 'n_bytes', default='0')
        try:
            flow['action'] = line.split('actions=')[1].strip()
        except IndexError:
            flow['action'] = 'N/A'
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
    clear_screen()
    print("=" * 75)
    print("           MULTI-SWITCH FLOW TABLE ANALYZER")
    print("=" * 75)
    print("Time:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print()

    total_flows = 0
    total_packets = 0

    for switch, flows in switches_data.items():
        print("-" * 75)
        print("  Switch: %s  |  Total Rules: %d" % (switch, len(flows)))
        print("-" * 75)
        print("  %-8s %-10s %-12s %-12s %-10s %-10s" %
              ("Rule#", "Priority", "Packets", "Bytes", "Type", "Status"))
        print("  " + "-" * 65)

        for i, flow in enumerate(flows):
            packets = int(flow['packets'].strip()) if flow['packets'].strip().isdigit() else 0
            total_packets += packets
            status = "ACTIVE" if packets > 0 else "UNUSED"
            marker = " >>" if packets > 0 else "   "
            print("%s%-5s %-10s %-12s %-12s %-10s %-10s" % (
                marker, str(i+1), flow['priority'],
                flow['packets'], flow['bytes'], flow['type'], status
            ))

        total_flows += len(flows)
        print()

    print("=" * 75)
    print("  SUMMARY")
    print("  Total Switches  : %d" % len(switches_data))
    print("  Total Rules     : %d" % total_flows)
    print("  Total Packets   : %d" % total_packets)
    print("  Active Rules    : %d" % sum(
        1 for flows in switches_data.values()
        for f in flows if f['packets'].strip().isdigit() and int(f['packets'].strip()) > 0
    ))
    print("  Unused Rules    : %d" % sum(
        1 for flows in switches_data.values()
        for f in flows if not f['packets'].strip().isdigit() or int(f['packets'].strip()) == 0
    ))
    print("=" * 75)

def run_analyzer(interval=5, rounds=5):
    print("Starting Flow Table Analyzer...")
    print("Querying every %d seconds for %d rounds" % (interval, rounds))
    time.sleep(2)

    for round_num in range(1, rounds + 1):
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
    parser = argparse.ArgumentParser(description='Multi-Switch Flow Table Analyzer')
    parser.add_argument('--interval', type=int, default=5,
                        help='Seconds between each poll (default: 5)')
    parser.add_argument('--rounds', type=int, default=5,
                        help='Number of polling rounds (default: 5)')
    args = parser.parse_args()
    run_analyzer(interval=args.interval, rounds=args.rounds)
