# Network Intrusion Detection System (IDS)

It is a lightweight Python script with graphical user interface (GUI) designed to monitor any activity on the network traffic and automatically alerts about potential flood attacks and modify the firewall. 

---

# Cloning Repository

To get local installation of the project, open terminal and run:
```bash
git clone https://github.com/Daemanic/ST4017CMD.git
cd ST4017CMD
```
---

# Required Installation

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

# Running the Program

The script requires ``sudo``/administrative priviledges to sniff network packets, for it to work run:
```bash
sudo python3 ids.py
```
For windows:
1. Open Powershell or CMD.
2. Right-click it and select ``Run as Administrator``.
3. Now, navigate to the folder and run: ``python3 ids.py``.

---

<img width="702" height="614" alt="image" src="https://github.com/user-attachments/assets/4000e52c-0c7a-4729-9ace-f314ee80ec15" />


