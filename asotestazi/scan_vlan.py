import os
import subprocess
import platform

def ping_host(ip):
    """
    Verifică dacă un IP răspunde la ping.
    :param ip: Adresa IP a hostului.
    :return: True dacă răspunde, False altfel.
    """
    # Selectăm comanda de ping în funcție de sistemul de operare
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def scan_network(ip_range):
    """
    Scanează rețeaua și returnează toate dispozitivele active.
    :param ip_range: Range-ul IP al rețelei (ex. '10.8.11.0/24')
    :return: O listă cu IP-urile dispozitivelor active.
    """
    # Extragem prefixul IP și numărul maxim de hosturi
    prefix = ip_range.rsplit('.', 1)[0]
    devices = []

    print("Scanning network...")

    # Iterăm prin toate posibilele adrese din subnet
    for i in range(1, 255):
        ip = f"{prefix}.{i}"
        if ping_host(ip):
            devices.append(ip)

    return devices

if __name__ == "__main__":
    # Definește range-ul IP (modifică în funcție de VLAN-ul tău)
    ip_range = "10.8.11.0/24"

    print(f"Scanning network {ip_range}...")
    devices = scan_network(ip_range)
    if devices:
        print("Active devices:")
        for ip in devices:
            print(f"IP: {ip}")
    else:
        print("No devices found.")

