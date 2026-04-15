# Name: Catherine D
# SRN: PES1UG24CS120
# Project: Multi-Switch Flow Table Analyzer
# Description: POX SDN Controller that installs flow rules and analyzes
#              flow table usage across multiple switches in Mininet

from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
import time

log = core.getLogger()

class FlowAnalyzerController(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        self.flow_stats = {}
        log.info("Flow Analyzer Controller started!")

    def _handle_ConnectionUp(self, event):
        dpid = dpidToStr(event.dpid)
        log.info("Switch %s connected" % dpid)
        self.flow_stats[dpid] = []
        self._install_flows(event)

    def _install_flows(self, event):
        dpid = dpidToStr(event.dpid)

        # Rule 1: ARP - flood
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.match.dl_type = 0x0806
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        log.info("[%s] Rule installed: ARP -> FLOOD" % dpid)

        # Rule 2: ICMP (ping) - flood
        msg = of.ofp_flow_mod()
        msg.priority = 90
        msg.match.dl_type = 0x0800
        msg.match.nw_proto = 1
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        log.info("[%s] Rule installed: ICMP -> FLOOD" % dpid)

        # Rule 3: TCP - flood
        msg = of.ofp_flow_mod()
        msg.priority = 80
        msg.match.dl_type = 0x0800
        msg.match.nw_proto = 6
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        log.info("[%s] Rule installed: TCP -> FLOOD" % dpid)

        # Rule 4: Default - flood everything else
        msg = of.ofp_flow_mod()
        msg.priority = 10
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)
        log.info("[%s] Rule installed: DEFAULT -> FLOOD" % dpid)

    def _handle_FlowStatsReceived(self, event):
        dpid = dpidToStr(event.connection.dpid)
        log.info("\n========== Flow Table: Switch %s ==========" % dpid)
        log.info("%-5s %-10s %-12s %-12s %-10s" % 
                ("Rule", "Priority", "Packets", "Bytes", "Type"))
        log.info("-" * 55)

        self.flow_stats[dpid] = event.stats

        for i, stat in enumerate(event.stats):
            if stat.match.dl_type == 0x0806:
                rule_type = "ARP"
            elif stat.match.dl_type == 0x0800 and stat.match.nw_proto == 1:
                rule_type = "ICMP"
            elif stat.match.dl_type == 0x0800 and stat.match.nw_proto == 6:
                rule_type = "TCP"
            else:
                rule_type = "DEFAULT"

            log.info("%-5s %-10s %-12s %-12s %-10s" % (
                str(i+1),
                str(stat.priority),
                str(stat.packet_count),
                str(stat.byte_count),
                rule_type
            ))
        log.info("==========================================\n")

    def _handle_PacketIn(self, event):
        dpid = dpidToStr(event.dpid)
        log.info("PacketIn from switch %s - requesting flow stats" % dpid)
        # request flow stats every time a packet_in occurs
        event.connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

def launch():
    core.registerNew(FlowAnalyzerController)
