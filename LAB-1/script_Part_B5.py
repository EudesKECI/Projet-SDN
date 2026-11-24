from mininet.topo import Topo

class LinkTopo( Topo ):
    "Topology with link and CPU parameters (Part B.5 - Figure 3)"

    def build( self ):
        # Création des hôtes avec limitation CPU pour h1
        # cpu=0.2 correspond aux 20% demandés sur la figure
        h1 = self.addHost( 'h1', ip='10.0.0.1', cpu=0.2 )
        h2 = self.addHost( 'h2', ip='10.0.0.2' )

        # Création du commutateur
        s1 = self.addSwitch( 's1' )

        # Création du lien standard entre h1 et s1
        self.addLink( h1, s1 )
        
        # Création du lien contraint entre s1 et h2
        # bw=10 (pour 10 Mbps) et delay='50ms'
        self.addLink( s1, h2, bw=10, delay='50ms' )

# Enregistrement pour l'interface en ligne de commande
topos = { 'linktopo': ( lambda: LinkTopo() ) }