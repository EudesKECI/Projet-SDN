#!/usr/bin/env python3
"""
M2 CCN - Lab 2: Exercise 2 - Breaking a network
Création d'une topologie avec une boucle sans Spanning Tree Protocol (STP).
"""

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def build_loop_network():
    # Instanciation de Mininet avec le contrôleur par défaut
    net = Mininet(controller=Controller, switch=OVSKernelSwitch)
    net.addController('c0')

    print("*** Création des switches (sans STP)...")
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    print("*** Création des hôtes...")
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    print("*** Connexion des hôtes aux switches...")
    net.addLink(h1, s1)
    net.addLink(h2, s2)

    print("*** Création de la BOUCLE physique (s1 <-> s2 <-> s3 <-> s1)...")
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, s1)

    print("*** Démarrage du réseau...")
    net.start()
    
    print("*** Lancement du CLI (Testez avec 'h1 ping h2')...")
    CLI(net)
    
    print("*** Arrêt du réseau...")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    build_loop_network()
