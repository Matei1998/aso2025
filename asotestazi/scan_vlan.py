import asyncio
import subprocess
import platform

async def ping_ip(ip):
    """Ping IP-ul pentru a verifica dacă este activ (asynchronous)."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    timeout = "-W 1"  # Timeout de 1 secundă pentru fiecare ping
    command = ["ping", param, "1", timeout, ip]
    
    process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await process.communicate()
    
    # Dacă ping-ul a avut succes (returncode 0)
    return process.returncode == 0

async def scan_network(ip_range):
    """Scanează rețeaua și returnează IP-urile active (asynchronous)."""
    tasks = []
    for i in range(1, 255):
        ip = f"{ip_range}.{i}"
        tasks.append(ping_ip(ip))
    
    results = await asyncio.gather(*tasks)
    active_ips = [f"{ip_range}.{i}" for i, result in enumerate(results, 1) if result]
    
    return active_ips

if __name__ == "__main__":
    # Definirea intervalului IP (se schimbă ultima parte a adresei IP pentru a scana între 1 și 254)
    ip_range = "10.8.11"  # IP-ul tău local (pe sub-rețeaua 10.8.11.0/24)
    
    print(f"Scanning network {ip_range}.0/24...")
    
    # Folosim asyncio.run pentru a rula scriptul
    active_ips = asyncio.run(scan_network(ip_range))
    
    if active_ips:
        print("Active devices found:")
        for ip in active_ips:
            print(f"IP: {ip}")
    else:
        print("No active devices found.")
