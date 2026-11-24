from mininet.topo import Topo

class MyTopo( Topo ):
    "Custom topology based on Lab 1, Figure 2"

    def build( self ):
        # Création des hôtes (avec assignation des adresses IP visibles sur le schéma)
        h3 = self.addHost( 'h3', ip='10.0.1.2/24' )
        h4 = self.addHost( 'h4', ip='10.0.1.3/24' )
        h5 = self.addHost( 'h5', ip='10.0.2.2/24' )

        # Création des switchs
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )

        # Création des liens
        self.addLink( h3, s1 )
        self.addLink( h4, s1 )
        self.addLink( s1, s2 )
        self.addLink( s2, h5 )

# Enregistrement pour l'interface en ligne de commande
topos = { 'mytopo': ( lambda: MyTopo() ) }