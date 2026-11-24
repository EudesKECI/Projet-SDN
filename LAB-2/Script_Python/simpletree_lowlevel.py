#!/usr/bin/env python3
"""
M2 CCN - Lab 2: Mininet
simpletree_lowlevel.py
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_simple_tree(n=2):
    # Instanciation explicite du réseau et du contrôleur par défaut
    net = Mininet(controller=Controller)
    net.addController('c0')

    print(f"*** Création de la topologie Tree bas niveau avec n={n}")
    
    # 1. Core Switch
    core = net.addSwitch('c1')

    # 2. Couches Aggregation, Edge et Hosts
    for i in range(n):
        agg_name = f'a{i+1}'
        agg = net.addSwitch(agg_name)
        net.addLink(agg, core)

        for j in range(n):
            edge_id = (i * n) + j + 1
            edge_name = f'e{edge_id}'
            edge = net.addSwitch(edge_name)
            net.addLink(edge, agg)

            for k in range(n):
                host_id = ((edge_id - 1) * n) + k + 1
                host_name = f'h{host_id}'
                host = net.addHost(host_name)
                net.addLink(host, edge)

    # Démarrage manuel des composants
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    
    user_input = input("Entrez la valeur de n (par défaut 2) : ")
    n = int(user_input) if user_input.isdigit() else 2
    
    create_simple_tree(n)
