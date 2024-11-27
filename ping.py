"""
ping.py : un simple Ping

un ping vers la passerelle du réseau
vous devez craft la trame entièrement à la main et utiliser la méthode srp() pour envoyer votre ptite trame
affiche dans le terminal le pong reçu
"""

from scapy.all import Ether, IP, ICMP, srp
import os

def get_default_gateway():
    return "10.3.0.1"

def craft_ping_trame():
    """
    Créer une trame Ping manuellement
    """
    gateway_ip = get_default_gateway()
    print(f"Passerelle par défaut : {gateway_ip}")

    # Couche Ethernet
    eth = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC (ou remplacer par une MAC spécifique)
    
    # Couche IP
    ip = IP(dst=gateway_ip)  # Adresse de destination : passerelle

    # Couche ICMP
    icmp = ICMP(type="echo-request")  # Ping (Echo Request)

    # Trame complète : Ethernet + IP + ICMP
    trame = eth / ip / icmp
    return trame

def send_ping(trame):
    """
    Envoyer une trame Ping et afficher la réponse
    """
    print("Envoi de la trame Ping...")
    response, _ = srp(trame, timeout=2, verbose=0)  # Envoyer la trame et attendre une réponse

    if response:
        for sent, received in response:
            print(f"Pong reçu de : {received[IP].src}")
            print(received.summary())
    else:
        print("Aucune réponse reçue.")

if __name__ == "__main__":
    print("Ping vers la passerelle réseau")
    trame_ping = craft_ping_trame()
    send_ping(trame_ping)
