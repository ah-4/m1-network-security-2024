
from scapy.all import sniff, TCP, IP

def process_packet(packet):
    """
    Callback pour traiter les paquets capturés.
    Vérifie si le paquet est un TCP SYN-ACK.
    """
    if TCP in packet and packet[TCP].flags == 0x12:  # SYN-ACK flag = 0x12
        print("TCP SYN ACK reçu !")
        print(f"- Adresse IP src : {packet[IP].src}")
        print(f"- Adresse IP dst : {packet[IP].dst}")
        print(f"- Port TCP src : {packet[TCP].sport}")
        print(f"- Port TCP dst : {packet[TCP].dport}")
        return True  # Indique que nous avons trouvé notre paquet

def main():
    """
    Fonction principale pour capturer les paquets TCP SYN-ACK.
    """
    print("En attente du premier TCP SYN-ACK...")
    sniff(filter="tcp", prn=process_packet, store=0, stop_filter=lambda p: TCP in p and p[TCP].flags == 0x12)

if __name__ == "__main__":
    main()
