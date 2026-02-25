import threading
import tkinter as tk
from tkinter import ttk
from scapy.layers.inet import IP
from scapy.all import sniff
import logging
import subprocess
import os

logging.basicConfig(filename="active.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class IDS_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aditya Shrestha - 250498")
        self.root.geometry("700x580")
        self.root.configure(bg="#252525")

        style = ttk.Style()
        style.configure("Vertical.TScrollbar",width=3,background="#353535",troughcolor="#1a1a1a",bordercolor="#1a1a1a",lightcolor="#1a1a1a",arrowsize=1)

        self.log_frame = tk.Frame(root, bg="#252525")
        self.log_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(self.log_frame,orient="vertical")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_display = tk.Text(self.log_frame,font=("Courier New", 13),width=80, height=25,state='disabled',bg="#252525",fg="#90EE90",borderwidth=0,highlightthickness=0,yscrollcommand=self.scrollbar.set)
        self.log_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.log_display.yview)

        self.packet_volume = []
        self.packet_count = 0
        self.whitelist = ["127.0.0.1", "8.8.8.8", "8.8.4.4"]

    def update_ui_log(self, message):
        logging.warning(message)
        self.log_display.configure(state='normal')
        self.log_display.insert(tk.END, message + "\n")
        self.log_display.configure(state='disabled')
        self.log_display.see(tk.END)

    def block_ip(self, ipadr):
        if ipadr in self.whitelist or ipadr.startswith("192.168."):
            return
        system_os = platform.system()
        try:
            if system_os == "Darwin":
                command = f"echo 'block drop in from {ipadr} to any' | sudo pfctl -f -"
            elif system_os == "Linux":
                command = f"sudo iptables -A INPUT -s {ipadr} -j DROP"
            elif system_os == "Windows":
                command = f"netsh advfirewall firewall add rule name='IDS_Block' dir=in action=block remoteip={ipadr}"
            subprocess.run(command, shell=True, check=True)
            self.update_ui_log(f"[!] Blocked {ipadr} on {system_os}")
        except Exception as error:
            self.update_ui_log(f"[!] Error blocking {ipadr}: {error}")

    def packet_callback(self, packet):
        if packet.haslayer(IP):
            ip_src = packet[IP].src
            packet_size = len(packet)
            self.packet_volume.append(packet_size)
            self.packet_count += 1
            if packet_size > 1500:
                self.update_ui_log(f"[!] Large Packet: {packet_size} bytes - {ip_src}")
            if self.packet_count > 100 and len(set(self.packet_volume[-100:])) == 1:
                self.update_ui_log(f"[!] Alert: flood detected - {ip_src}")
                self.block_ip(ip_src)

    def start_sniffing(self):
        sniff(prn=self.packet_callback, store=0)

if __name__ == "__main__":
    if os.getuid() != 0:
        print("[!] Error: <sudo> privilege required")
        exit()
    root = tk.Tk()
    app = IDS_GUI(root)
    threading.Thread(target=app.start_sniffing, daemon=True).start()
    root.mainloop()
