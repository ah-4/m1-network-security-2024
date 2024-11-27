from scapy.all import sniff, DNS, DNSQR, DNSRR, IP, sr1, UDP
import time

def send_dns_query():
    """
    Envoie une requête DNS pour 'efrei.fr'.
    """
    print("Envoi de la requête DNS pour efrei.fr...")
    dns_request = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="efrei.fr"))
    sr1(dns_request, verbose=0)  # Envoi de la requête et attente de la réponse


def process_packet(packet):
    """
    Callback pour traiter les paquets capturés.
    Vérifie si le paquet est une réponse DNS pour efrei.fr.
    """
    if packet.haslayer(DNS) and packet.getlayer(DNS).ancount > 0:  # Vérifie si c'est une réponse DNS
        query_name = packet[DNSQR].qname.decode("utf-8").strip(".")
        if query_name == "efrei.fr":  # Filtrer les requêtes pour efrei.fr
            # Obtenir les réponses DNS (adresses IP)
            print("Réponse DNS reçue pour efrei.fr :")
            for i in range(packet[DNS].ancount):
                dns_rr = packet[DNS].an[i]  # Réponse DNS individuelle
                if dns_rr.type == 1:  # Type A (IPv4)
                    print(f"- Adresse IP : {dns_rr.rdata}")
            return True  # Arrêter après avoir capturé la réponse pour efrei.fr


def main():
    """
    Fonction principale pour envoyer une requête DNS et capturer la réponse.
    """
    print("Capture DNS pour efrei.fr...")
    # Lancer la capture en arrière-plan
    sniff_thread = sniff(
        filter="udp port 53",
        prn=process_packet,
        store=0,
        stop_filter=lambda p: p.haslayer(DNS) and p.getlayer(DNS).ancount > 0,
        timeout=10
    )
    
    # Envoyer la requête DNS
    send_dns_query()

    # Attendre un instant pour capturer la réponse
    time.sleep(2)
    print("Capture terminée.")


if __name__ == "__main__":
    main()
