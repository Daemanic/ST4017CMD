# 🌐 Network Intrusion Detection System (IDS)

It is a lightweight Python script with graphical user interface (GUI) designed to monitor any activity on the network traffic and automatically alerts about potential flood attacks and modify the firewall. By utilizing threading, the program maintains a responsive user interface while simultaneously performing deep packet inspection in the background, ensuring no high-spped traffic enters the network. The script mainly focuses on changing from passive observer to an active defender which makes the script a practical example of **Automated Incident Response**. 

---

# [?] Cloning Repository

To get local installation of the project, open terminal and run:
```bash
git clone https://github.com/Daemanic/ST4017CMD.git
cd ST4017CMD
```
---

# [?] Required Installation

The Python code uses libraries such as Scapy for packet manipulation and Tkinter for UI generation. Ensure Python3 is installed and check for the libraries by running:
Using pip:
```bash
pip install scapy tk
```
If gives ``command not found`` error, use this shortcut:
```bash
python3 -m pip instal scapy tk
```

Note: Tkinter might give an error saying ``tk`` or ``tkinter`` not found:
- MacOS: usually has it pre-installed. If missing, use ``brew install python-tk``.
- Linux: run ``sudo apt-get install python3-tk``.
- Windows: ``re-run`` the python installer and proceed.

---

# [?] Running the Program

The script requires ``sudo``/administrative priviledges to sniff network packets, for it to work run:
```bash
sudo python3 ids.py
```
For windows:
1. Open Powershell or CMD.
2. Right-click it and select ``Run as Administrator``.
3. Now, navigate to the folder and run: ``python3 ids.py``.

---

# [?] Code Functionality

**1. GUI Layer (IDS_GUI)**
The interface is built with ``Tkinter``, using threaded approach. It ensures the window remains responsive while the code actively runs in the background.

**2. Sniffing Engine (scapy)**
The code utilizes sniff() function to capture live packets being transmitted and recieved. It extracts the ``Source IP`` and ``Packet Size`` for every incoming transmission. The detection logic followed behind is:
- Large Packet Alert: flags any packet over 1500 bytes.
- Flood Detection: if the last 100 packets are indentical in size, the system identifies it as a potential automated DoS/Flood attack.

**3. Universal Mitigation (pfctl, iptables, netsh)**
According to the operation system (MacOS, Linux or Windows) it applies the corresponding firewall commad. Once a flood is detected, it adds a temporary rule to block all incoming traffic from attacker's IP address.

**Note: Maintainance & Reset:**
To clear blocked IPs, run one of these commands:
- MacOS: ``sudo pfctl -F all -f /etc/pf.conf``
- Linux: ``sudo iptables -F``
- Windows: Open ``Windows Defender Firewall with Advanced Security`` and remove the ``IDS_Block`` rules.

---

<img width="702" height="614" alt="image" src="https://github.com/user-attachments/assets/4000e52c-0c7a-4729-9ace-f314ee80ec15" />






