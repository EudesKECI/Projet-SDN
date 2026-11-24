"""
Exercice 3 - Multipath Routing avec POX

Strategie :
- Broadcast et multicast sur un arbre sans boucle
- Unicast sur des chemins statiques differents
- Installation de regles OpenFlow
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# Adresses MAC des quatre hotes
HOST_MAC = {
    1: "00:00:00:00:10:01",
    2: "00:00:00:00:20:01",
    3: "00:00:00:00:30:01",
    4: "00:00:00:00:40:01"
}

# Table de routage statique : switch -> destination -> port de sortie
ROUTES = {
    1: {1: 1, 2: 3, 3: 3, 4: 2},
    2: {1: 3, 2: 1, 3: 2, 4: 3},
    3: {1: 3, 2: 2, 3: 1, 4: 3},
    4: {1: 2, 2: 3, 3: 3, 4: 1}
}

# Arbre de diffusion pour les broadcasts (Lien s3-s4 exclu pour casser la boucle)
BROADCAST_PORTS = {
    1: [1, 2, 3],
    2: [1, 2, 3],
    3: [1, 2],
    4: [1, 2]
}

class Diamond(object):

    def __init__(self, connection):
        self.connection = connection
        self.dpid = connection.dpid
        connection.addListeners(self)
        self.mac_to_port = {}
        log.info("Switch s%s connected to POX", self.dpid)

    # CORRECTION : La fonction doit être indentée à l'intérieur de la classe
    def resend_packet(self, packet_in, out_port):
        msg = of.ofp_packet_out()
        
        # On copie la payload brute pour s'affranchir du buffer
        msg.data = packet_in.data
        
        # On indique explicitement l'absence de buffer
        msg.buffer_id = of.NO_BUFFER
        msg.in_port = packet_in.in_port
        
        msg.actions.append(
            of.ofp_action_output(port=out_port)
        )
        self.connection.send(msg)

    def act_like_hub(self, packet, packet_in):
        self.resend_packet(packet_in, of.OFPP_ALL)

    def act_less_stupidly(self, packet, packet_in):
        switch_id = self.dpid
        in_port = packet_in.in_port

        if switch_id not in ROUTES:
            log.warning("Unknown switch: %s", switch_id)
            return

        self.mac_to_port[str(packet.src)] = in_port

        # ------------------------------
        # BROADCAST / MULTICAST
        # ------------------------------
        if packet.dst.is_multicast:
            allowed_ports = BROADCAST_PORTS[switch_id]
            if in_port not in allowed_ports:
                return

            for port in allowed_ports:
                if port != in_port:
                    self.resend_packet(packet_in, port)
            return

        # ------------------------------
        # UNICAST
        # ------------------------------
        destination = str(packet.dst).lower()
        host_id = None

        for h, mac in HOST_MAC.items():
            if destination == mac:
                host_id = h
                break

        if host_id is None:
            log.warning("Unknown destination MAC: %s", destination)
            return

        out_port = ROUTES[switch_id][host_id]

        if out_port == in_port:
            return

        log.info("s%s: destination h%s -> port %s", switch_id, host_id, out_port)

        # Installation de la règle OpenFlow
        msg = of.ofp_flow_mod()
        msg.priority = 100
        msg.idle_timeout = 60
        msg.hard_timeout = 0
        msg.match = of.ofp_match(dl_dst=packet.dst)
        msg.actions.append(of.ofp_action_output(port=out_port))
        self.connection.send(msg)

        # Transmission du paquet actuel
        self.resend_packet(packet_in, out_port)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            log.warning("Incomplete packet")
            return

        packet_in = event.ofp
        self.act_less_stupidly(packet, packet_in)


def launch():
    log.info("Custom multipath component loaded")
    def start_switch(event):
        Diamond(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)