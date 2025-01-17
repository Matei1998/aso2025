from scapy.all import ARP, Ether, srp

def scan_network(ip_range):
    """
    Scanează rețeaua și returnează toate dispozitivele active.
    :param ip_range: Range-ul IP al rețelei (ex. '192.168.1.0/24')
    :return: O listă cu IP-urile și MAC-urile dispozitivelor active
    """
    # Creăm un pachet ARP pentru scanare
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    # Trimitem pachetul și primim răspunsurile
    result = srp(packet, timeout=2, verbose=False)[0]

    # Extragem IP-urile și MAC-urile
    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    return devices

if __name__ == "__main__":
    # Definește range-ul IP (modifică în funcție de VLAN-ul tău)
    ip_range = "192.168.1.0/24"

    print(f"Scanning network {ip_range}...")
    devices = scan_network(ip_range)
    if devices:
        print("Active devices:")
        for device in devices:
            print(f"IP: {device['ip']}, MAC: {device['mac']}")
    else:
        print("No devices found.")
