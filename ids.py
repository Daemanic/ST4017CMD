import threading
import tkinter as tk
from tkinter import ttk
from scapy.layers.inet import IP
from scapy.all import sniff
import logging
import subprocess
import platform
import os
import sys

logging.basicConfig(filename="active.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class IDS_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ST4017CMD - 250498")
        self.root.geometry("700x580")
        self.root.configure(bg="#252525")
        style = ttk.Style()
        style.configure("Vertical.TScrollbar", width=3)
        self.log_frame = tk.Frame(root, bg="#252525")
        self.log_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_display = tk.Text(
            self.log_frame,
            font=("Courier New", 13),
            width=80,
            height=25,
            state='disabled',
            bg="#252525",
            fg="#90EE90",
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=self.scrollbar.set)
        self.log_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.log_display.yview)
        self.packet_volume = []
        self.packet_count = 0
        self.whitelist = ["127.0.0.1"]

    def update_ui_log(self, message):
        logging.warning(message)
        def write():
            self.log_display.configure(state='normal')
            self.log_display.insert(tk.END, message + "\n")
            self.log_display.configure(state='disabled')
            self.log_display.see(tk.END)
        self.root.after(0, write)

    def safe_ip(self, ipadr):
        if ipadr in self.whitelist:
            return True
        if ipadr.startswith("192.168."):
            return True
        return False

    def block_ip(self, ipadr):
        if self.safe_ip(ipadr):
            return
        system_os = platform.system()
        command = None
        try:
            if system_os == "Darwin":
                command = f"echo 'block drop from {ipadr} to any' | sudo pfctl -f -"

            elif system_os == "Linux":
                command = f"sudo iptables -I INPUT -s {ipadr} -j DROP"

            elif system_os == "Windows":
                command = f"netsh advfirewall firewall add rule name=IDS_Block_{ipadr} dir=in action=block remoteip={ipadr}"

            if command:
                subprocess.run(command, shell=True)
                self.update_ui_log(f"[!] Blocked {ipadr} on {system_os}")
            else:
                self.update_ui_log(f"[?] OS {system_os} not supported")

        except Exception as error:
            self.update_ui_log(f"[!] Error blocking {ipadr}: {error}")

    def packet_callback(self, packet):
        if packet.haslayer(IP):
            ip_src = packet[IP].src
            if self.safe_ip(ip_src):
                return
            packet_size = len(packet)
            self.packet_volume.append(packet_size)
            self.packet_count += 1
            if packet_size > 1500:
                self.update_ui_log(f"[!] Large Packet: {packet_size} bytes - {ip_src}")

            if self.packet_count > 100:
                recent = self.packet_volume[-100:]
                if sum(recent) / len(recent) > 1000:
                    self.update_ui_log(f"[!] Possible flood detected - {ip_src}")
                    self.block_ip(ip_src)

    def start_sniffing(self):
        sniff(prn=self.packet_callback, store=0)

if __name__ == "__main__":
    if platform.system() != "Windows":
        if os.geteuid() != 0:
            print("[!] Run with sudo")
            sys.exit()
    root = tk.Tk()
    app = IDS_GUI(root)
    threading.Thread(target=app.start_sniffing, daemon=True).start()
    root.mainloop()
