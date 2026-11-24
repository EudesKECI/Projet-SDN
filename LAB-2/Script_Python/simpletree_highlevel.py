#!/usr/bin/env python3
"""
simpletree_highlevel.py
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

class SimpleTreeTopo(Topo):
    def build(self, n=2):
        # 1. Création du Core Switch
        core = self.addSwitch('c1')

        # 2. Création de la couche d'Aggregation
        for i in range(n):
            agg_name = f'a{i+1}'
            agg = self.addSwitch(agg_name)
            self.addLink(agg, core)

            # 3. Création de la couche Edge
            for j in range(n):
                edge_id = (i * n) + j + 1
                edge_name = f'e{edge_id}'
                edge = self.addSwitch(edge_name)
                self.addLink(edge, agg)

                # 4. Création des Hosts (Serveurs)
                for k in range(n):
                    host_id = ((edge_id - 1) * n) + k + 1
                    host_name = f'h{host_id}'
                    host = self.addHost(host_name)
                    self.addLink(host, edge)

if __name__ == '__main__':
    setLogLevel('info')
    
    # Récupération de la valeur n en input
    user_input = input("Entrez la valeur de n (par défaut 2) : ")
    n = int(user_input) if user_input.isdigit() else 2
    
    print(f"*** Création de la topologie Tree avec n={n}")
    topo = SimpleTreeTopo(n=n)
    
    # Instanciation de Mininet avec la topologie de haut niveau
    net = Mininet(topo=topo)
    
    net.start()
    CLI(net)
    net.stop()
