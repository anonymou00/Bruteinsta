import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import subprocess
import socket
import nmap
import scapy.all as scapy
import requests
import json
import os
import sys
from datetime import datetime
import queue
import time

class ModernPenetrationToolkit:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modern Penetration Testing Toolkit")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Modern.TFrame', background='#2b2b2b')
        self.style.configure('Modern.TLabel', background='#2b2b2b', foreground='#ffffff')
        self.style.configure('Modern.TButton', background='#4a90e2', foreground='#ffffff')
        
        self.setup_ui()
        self.scan_results = {}
        self.attack_queue = queue.Queue()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, style='Modern.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Modern Penetration Testing Toolkit", 
                              font=('Arial', 20, 'bold'), bg='#2b2b2b', fg='#4a90e2')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Network Reconnaissance Tab
        self.create_network_tab()
        
        # Wireless Attacks Tab
        self.create_wireless_tab()
        
        # Web Application Tab
        self.create_web_tab()
        
        # System Exploitation Tab
        self.create_system_tab()
        
        # Social Engineering Tab
        self.create_social_tab()
        
        # Log Tab
        self.create_log_tab()
        
    def create_network_tab(self):
        network_frame = ttk.Frame(self.notebook)
        self.notebook.add(network_frame, text="Network Reconnaissance")
        
        # Network scan section
        scan_frame = tk.LabelFrame(network_frame, text="Network Scanning", 
                                  bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        scan_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Target input
        tk.Label(scan_frame, text="Target Network:", bg='#2b2b2b', fg='#ffffff').pack(anchor=tk.W, padx=10, pady=5)
        self.target_entry = tk.Entry(scan_frame, width=30, bg='#3c3c3c', fg='#ffffff')
        self.target_entry.pack(anchor=tk.W, padx=10, pady=5)
        self.target_entry.insert(0, "192.168.1.0/24")
        
        # Scan buttons
        button_frame = tk.Frame(scan_frame, bg='#2b2b2b')
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="Quick Scan", command=self.quick_network_scan,
                 bg='#4a90e2', fg='#ffffff', relief=tk.FLAT, padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Full Scan", command=self.full_network_scan,
                 bg='#e74c3c', fg='#ffffff', relief=tk.FLAT, padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Port Scan", command=self.port_scan,
                 bg='#f39c12', fg='#ffffff', relief=tk.FLAT, padx=20, pady=5).pack(side=tk.LEFT, padx=5)
        
        # Results area
        results_frame = tk.LabelFrame(network_frame, text="Scan Results", 
                                     bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.network_results = scrolledtext.ScrolledText(results_frame, bg='#1e1e1e', fg='#00ff00', 
                                                        font=('Consolas', 10))
        self.network_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_wireless_tab(self):
        wireless_frame = ttk.Frame(self.notebook)
        self.notebook.add(wireless_frame, text="Wireless Attacks")
        
        # WiFi scan section
        wifi_frame = tk.LabelFrame(wireless_frame, text="WiFi Network Discovery", 
                                  bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        wifi_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(wifi_frame, text="Scan WiFi Networks", command=self.scan_wifi_networks,
                 bg='#4a90e2', fg='#ffffff', relief=tk.FLAT, padx=20, pady=5).pack(pady=10)
        
        # WiFi results
        wifi_results_frame = tk.LabelFrame(wireless_frame, text="Available Networks", 
                                          bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        wifi_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.wifi_tree = ttk.Treeview(wifi_results_frame, columns=('SSID', 'BSSID', 'Channel', 'Signal', 'Security'), 
                                     show='headings')
        self.wifi_tree.heading('SSID', text='SSID')
        self.wifi_tree.heading('BSSID', text='BSSID')
        self.wifi_tree.heading('Channel', text='Channel')
        self.wifi_tree.heading('Signal', text='Signal')
        self.wifi_tree.heading('Security', text='Security')
        self.wifi_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Attack options
        attack_frame = tk.LabelFrame(wireless_frame, text="Attack Options", 
                                    bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        attack_frame.pack(fill=tk.X, padx=10, pady=10)
        
        attack_buttons = [
            ("Deauthentication Attack", self.deauth_attack),
            ("Evil Twin Attack", self.evil_twin_attack),
            ("WPS Brute Force", self.wps_brute_force),
            ("WPA/WPA2 Cracking", self.wpa_cracking)
        ]
        
        for text, command in attack_buttons:
            tk.Button(attack_frame, text=text, command=command,
                     bg='#e74c3c', fg='#ffffff', relief=tk.FLAT, padx=20, pady=5).pack(pady=5)
        
    def create_web_tab(self):
        web_frame = ttk.Frame(self.notebook)
        self.notebook.add(web_frame, text="Web Application")
        
        # Target URL input
        url_frame = tk.LabelFrame(web_frame, text="Target URL", 
                                 bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        url_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(url_frame, text="URL:", bg='#2b2b2b', fg='#ffffff').pack(anchor=tk.W, padx=10, pady=5)
        self.url_entry = tk.Entry(url_frame, width=50, bg='#3c3c3c', fg='#ffffff')
        self.url_entry.pack(anchor=tk.W, padx=10, pady=5)
        self.url_entry.insert(0, "http://example.com")
        
        # Web attack options
        web_attacks_frame = tk.LabelFrame(web_frame, text="Web Application Attacks", 
                                         bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        web_attacks_frame.pack(fill=tk.X, padx=10, pady=10)
        
        web_attack_buttons = [
            ("SQL Injection Scanner", self.sql_injection_scan),
            ("XSS Scanner", self.xss_scan),
            ("Directory Traversal", self.directory_traversal),
            ("CSRF Scanner", self.csrf_scan),
            ("Open Redirect Scanner", self.open_redirect_scan)
        ]
        
        for text, command in web_attack_buttons:
            tk.Button(web_attacks_frame, text=text, command=command,
                     bg='#e74c3c', fg='#ffffff', relief=tk.FLAT, padx=20, pady=5).pack(pady=5)
        
        # Web results
        web_results_frame = tk.LabelFrame(web_frame, text="Scan Results", 
                                         bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        web_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.web_results = scrolledtext.ScrolledText(web_results_frame, bg='#1e1e1e', fg='#00ff00', 
                                                    font=('Consolas', 10))
        self.web_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_system_tab(self):
        system_frame = ttk.Frame(self.notebook)
        self.notebook.add(system_frame, text="System Exploitation")
        
        # System info
        info_frame = tk.LabelFrame(system_frame, text="System Information", 
                                  bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(info_frame, text="Get System Info", command=self.get_system_info,
                 bg='#4a90e2', fg='#ffffff', relief=tk.FLAT, padx=20, pady=5).pack(pady=10)
        
        # System attacks
        sys_attacks_frame = tk.LabelFrame(system_frame, text="System Attacks", 
                                         bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        sys_attacks_frame.pack(fill=tk.X, padx=10, pady=10)
        
        sys_attack_buttons = [
            ("Privilege Escalation Check", self.privilege_escalation_check),
            ("UAC Bypass Attempt", self.uac_bypass_attempt),
            ("Registry Analysis", self.registry_analysis),
            ("Process Injection Check", self.process_injection_check)
        ]
        
        for text, command in sys_attack_buttons:
            tk.Button(sys_attacks_frame, text=text, command=command,
                     bg='#e74c3c', fg='#ffffff', relief=tk.FLAT, padx=20, pady=5).pack(pady=5)
        
        # System results
        sys_results_frame = tk.LabelFrame(system_frame, text="Results", 
                                         bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        sys_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.system_results = scrolledtext.ScrolledText(sys_results_frame, bg='#1e1e1e', fg='#00ff00', 
                                                       font=('Consolas', 10))
        self.system_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_social_tab(self):
        social_frame = ttk.Frame(self.notebook)
        self.notebook.add(social_frame, text="Social Engineering")
        
        # Social engineering tools
        social_tools_frame = tk.LabelFrame(social_frame, text="Social Engineering Tools", 
                                          bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        social_tools_frame.pack(fill=tk.X, padx=10, pady=10)
        
        social_buttons = [
            ("Email Spoofing Test", self.email_spoofing_test),
            ("Phishing Page Generator", self.phishing_page_generator),
            ("QR Code Generator", self.qr_code_generator),
            ("Social Media Recon", self.social_media_recon)
        ]
        
        for text, command in social_buttons:
            tk.Button(social_tools_frame, text=text, command=command,
                     bg='#e74c3c', fg='#ffffff', relief=tk.FLAT, padx=20, pady=5).pack(pady=5)
        
        # Social results
        social_results_frame = tk.LabelFrame(social_frame, text="Results", 
                                            bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        social_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.social_results = scrolledtext.ScrolledText(social_results_frame, bg='#1e1e1e', fg='#00ff00', 
                                                       font=('Consolas', 10))
        self.social_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_log_tab(self):
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="Activity Log")
        
        # Log area
        log_area_frame = tk.LabelFrame(log_frame, text="Activity Log", 
                                       bg='#2b2b2b', fg='#ffffff', font=('Arial', 12, 'bold'))
        log_area_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_area_frame, bg='#1e1e1e', fg='#00ff00', 
                                                 font=('Consolas', 10))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Clear log button
        tk.Button(log_frame, text="Clear Log", command=self.clear_log,
                 bg='#e74c3c', fg='#ffffff', relief=tk.FLAT, padx=20, pady=5).pack(pady=10)
        
    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        
    # Network scanning methods
    def quick_network_scan(self):
        def scan():
            target = self.target_entry.get()
            self.log_message(f"Starting quick network scan on {target}")
            
            try:
                # Simulate network scan
                nm = nmap.PortScanner()
                nm.scan(hosts=target, arguments='-sn')
                
                results = "Quick Network Scan Results:\n"
                results += "=" * 50 + "\n"
                
                for host in nm.all_hosts():
                    if nm[host].state() == 'up':
                        results += f"Host: {host} - Status: UP\n"
                        if 'mac' in nm[host]['addresses']:
                            results += f"MAC: {nm[host]['addresses']['mac']}\n"
                        if 'vendor' in nm[host]['addresses']:
                            results += f"Vendor: {nm[host]['addresses']['vendor']}\n"
                        results += "-" * 30 + "\n"
                
                self.network_results.delete(1.0, tk.END)
                self.network_results.insert(tk.END, results)
                self.log_message("Quick network scan completed")
                
            except Exception as e:
                self.log_message(f"Error during network scan: {str(e)}")
                
        threading.Thread(target=scan, daemon=True).start()
        
    def full_network_scan(self):
        def scan():
            target = self.target_entry.get()
            self.log_message(f"Starting full network scan on {target}")
            
            try:
                # Simulate comprehensive scan
                nm = nmap.PortScanner()
                nm.scan(hosts=target, arguments='-sS -sV -O')
                
                results = "Full Network Scan Results:\n"
                results += "=" * 50 + "\n"
                
                for host in nm.all_hosts():
                    if nm[host].state() == 'up':
                        results += f"Host: {host}\n"
                        results += f"Status: {nm[host].state()}\n"
                        
                        if 'osmatch' in nm[host]:
                            for os in nm[host]['osmatch']:
                                results += f"OS: {os['name']} (Accuracy: {os['accuracy']}%)\n"
                        
                        if 'tcp' in nm[host]:
                            for port in nm[host]['tcp']:
                                service = nm[host]['tcp'][port]
                                results += f"Port {port}: {service['state']} - {service['name']} - {service['product']}\n"
                        
                        results += "-" * 30 + "\n"
                
                self.network_results.delete(1.0, tk.END)
                self.network_results.insert(tk.END, results)
                self.log_message("Full network scan completed")
                
            except Exception as e:
                self.log_message(f"Error during full scan: {str(e)}")
                
        threading.Thread(target=scan, daemon=True).start()
        
    def port_scan(self):
        def scan():
            target = self.target_entry.get()
            self.log_message(f"Starting port scan on {target}")
            
            try:
                # Common ports to scan
                common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5900, 8080]
                
                results = "Port Scan Results:\n"
                results += "=" * 50 + "\n"
                
                for port in common_ports:
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        result = sock.connect_ex((target.split('/')[0], port))
                        if result == 0:
                            service = socket.getservbyport(port, "tcp")
                            results += f"Port {port}: OPEN - {service}\n"
                        sock.close()
                    except:
                        pass
                
                self.network_results.delete(1.0, tk.END)
                self.network_results.insert(tk.END, results)
                self.log_message("Port scan completed")
                
            except Exception as e:
                self.log_message(f"Error during port scan: {str(e)}")
                
        threading.Thread(target=scan, daemon=True).start()
        
    # Wireless attack methods
    def scan_wifi_networks(self):
        def scan():
            self.log_message("Starting WiFi network scan")
            
            try:
                # Simulate WiFi scan using Windows commands
                result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], 
                                      capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    self.log_message("WiFi scan completed successfully")
                    # Parse and display results
                    self.parse_wifi_results(result.stdout)
                else:
                    self.log_message("WiFi scan failed")
                    
            except Exception as e:
                self.log_message(f"Error during WiFi scan: {str(e)}")
                
        threading.Thread(target=scan, daemon=True).start()
        
    def parse_wifi_results(self, output):
        # Clear existing items
        for item in self.wifi_tree.get_children():
            self.wifi_tree.delete(item)
            
        # Parse the output and add to treeview
        lines = output.split('\n')
        current_ssid = ""
        current_bssid = ""
        current_channel = ""
        current_signal = ""
        current_security = ""
        
        for line in lines:
            line = line.strip()
            if "SSID" in line and "BSSID" not in line:
                current_ssid = line.split(":")[1].strip() if ":" in line else ""
            elif "BSSID" in line:
                current_bssid = line.split(":")[1].strip() if ":" in line else ""
            elif "Channel" in line:
                current_channel = line.split(":")[1].strip() if ":" in line else ""
            elif "Signal" in line:
                current_signal = line.split(":")[1].strip() if ":" in line else ""
            elif "Authentication" in line:
                current_security = line.split(":")[1].strip() if ":" in line else ""
                if current_ssid and current_bssid:
                    self.wifi_tree.insert('', 'end', values=(current_ssid, current_bssid, 
                                                            current_channel, current_signal, current_security))
                    
    def deauth_attack(self):
        self.log_message("Deauthentication attack simulation started")
        messagebox.showwarning("Warning", "This is a simulation. Real deauth attacks require proper authorization.")
        
    def evil_twin_attack(self):
        self.log_message("Evil twin attack simulation started")
        messagebox.showwarning("Warning", "This is a simulation. Real evil twin attacks require proper authorization.")
        
    def wps_brute_force(self):
        self.log_message("WPS brute force simulation started")
        messagebox.showwarning("Warning", "This is a simulation. Real WPS attacks require proper authorization.")
        
    def wpa_cracking(self):
        self.log_message("WPA cracking simulation started")
        messagebox.showwarning("Warning", "This is a simulation. Real WPA attacks require proper authorization.")
        
    # Web application methods
    def sql_injection_scan(self):
        def scan():
            url = self.url_entry.get()
            self.log_message(f"Starting SQL injection scan on {url}")
            
            # Common SQL injection payloads
            payloads = ["'", "1' OR '1'='1", "1' AND '1'='2", "'; DROP TABLE users; --"]
            
            results = "SQL Injection Scan Results:\n"
            results += "=" * 50 + "\n"
            
            for payload in payloads:
                try:
                    test_url = f"{url}?id={payload}"
                    response = requests.get(test_url, timeout=5)
                    
                    # Check for common SQL error messages
                    sql_errors = ["sql syntax", "mysql_fetch", "oracle", "sql server", "postgresql"]
                    for error in sql_errors:
                        if error.lower() in response.text.lower():
                            results += f"Potential SQL injection found with payload: {payload}\n"
                            results += f"Error detected: {error}\n"
                            break
                            
                except Exception as e:
                    results += f"Error testing payload {payload}: {str(e)}\n"
                    
            self.web_results.delete(1.0, tk.END)
            self.web_results.insert(tk.END, results)
            self.log_message("SQL injection scan completed")
            
        threading.Thread(target=scan, daemon=True).start()
        
    def xss_scan(self):
        def scan():
            url = self.url_entry.get()
            self.log_message(f"Starting XSS scan on {url}")
            
            # Common XSS payloads
            payloads = [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "javascript:alert('XSS')",
                "<svg onload=alert('XSS')>"
            ]
            
            results = "XSS Scan Results:\n"
            results += "=" * 50 + "\n"
            
            for payload in payloads:
                try:
                    test_url = f"{url}?q={payload}"
                    response = requests.get(test_url, timeout=5)
                    
                    if payload in response.text:
                        results += f"Potential XSS found with payload: {payload}\n"
                        
                except Exception as e:
                    results += f"Error testing payload {payload}: {str(e)}\n"
                    
            self.web_results.delete(1.0, tk.END)
            self.web_results.insert(tk.END, results)
            self.log_message("XSS scan completed")
            
        threading.Thread(target=scan, daemon=True).start()
        
    def directory_traversal(self):
        def scan():
            url = self.url_entry.get()
            self.log_message(f"Starting directory traversal scan on {url}")
            
            # Common directory traversal payloads
            payloads = [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
                "....//....//....//etc/passwd",
                "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
            ]
            
            results = "Directory Traversal Scan Results:\n"
            results += "=" * 50 + "\n"
            
            for payload in payloads:
                try:
                    test_url = f"{url}?file={payload}"
                    response = requests.get(test_url, timeout=5)
                    
                    # Check for common file contents
                    if "root:" in response.text or "Administrator" in response.text:
                        results += f"Potential directory traversal found with payload: {payload}\n"
                        
                except Exception as e:
                    results += f"Error testing payload {payload}: {str(e)}\n"
                    
            self.web_results.delete(1.0, tk.END)
            self.web_results.insert(tk.END, results)
            self.log_message("Directory traversal scan completed")
            
        threading.Thread(target=scan, daemon=True).start()
        
    def csrf_scan(self):
        self.log_message("CSRF scan simulation started")
        messagebox.showinfo("Info", "CSRF scan simulation completed")
        
    def open_redirect_scan(self):
        self.log_message("Open redirect scan simulation started")
        messagebox.showinfo("Info", "Open redirect scan simulation completed")
        
    # System exploitation methods
    def get_system_info(self):
        def get_info():
            self.log_message("Getting system information")
            
            try:
                results = "System Information:\n"
                results += "=" * 50 + "\n"
                
                # Get OS info
                import platform
                results += f"OS: {platform.system()} {platform.release()}\n"
                results += f"Architecture: {platform.machine()}\n"
                results += f"Hostname: {platform.node()}\n"
                
                # Get user info
                import getpass
                results += f"Current User: {getpass.getuser()}\n"
                
                # Get network info
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                results += f"Local IP: {local_ip}\n"
                
                self.system_results.delete(1.0, tk.END)
                self.system_results.insert(tk.END, results)
                self.log_message("System information retrieved")
                
            except Exception as e:
                self.log_message(f"Error getting system info: {str(e)}")
                
        threading.Thread(target=get_info, daemon=True).start()
        
    def privilege_escalation_check(self):
        self.log_message("Privilege escalation check simulation started")
        messagebox.showinfo("Info", "Privilege escalation check simulation completed")
        
    def uac_bypass_attempt(self):
        self.log_message("UAC bypass attempt simulation started")
        messagebox.showinfo("Info", "UAC bypass attempt simulation completed")
        
    def registry_analysis(self):
        self.log_message("Registry analysis simulation started")
        messagebox.showinfo("Info", "Registry analysis simulation completed")
        
    def process_injection_check(self):
        self.log_message("Process injection check simulation started")
        messagebox.showinfo("Info", "Process injection check simulation completed")
        
    # Social engineering methods
    def email_spoofing_test(self):
        self.log_message("Email spoofing test simulation started")
        messagebox.showinfo("Info", "Email spoofing test simulation completed")
        
    def phishing_page_generator(self):
        self.log_message("Phishing page generator simulation started")
        messagebox.showinfo("Info", "Phishing page generator simulation completed")
        
    def qr_code_generator(self):
        self.log_message("QR code generator simulation started")
        messagebox.showinfo("Info", "QR code generator simulation completed")
        
    def social_media_recon(self):
        self.log_message("Social media reconnaissance simulation started")
        messagebox.showinfo("Info", "Social media reconnaissance simulation completed")
        
    def run(self):
        self.log_message("Modern Penetration Testing Toolkit started")
        self.root.mainloop()

if __name__ == "__main__":
    # Check if running on Windows
    if sys.platform != "win32":
        print("This tool is designed to run on Windows only.")
        sys.exit(1)
        
    # Show disclaimer
    disclaimer = """
    ⚠️  DISCLAIMER ⚠️
    
    This tool is for EDUCATIONAL PURPOSES ONLY.
    
    - Only use on systems you own or have explicit permission to test
    - Unauthorized penetration testing is illegal
    - The developers are not responsible for any misuse
    - This tool demonstrates security concepts for learning
    
    By using this tool, you agree to use it responsibly and legally.
    """
    
    print(disclaimer)
    response = input("Do you agree to use this tool responsibly? (yes/no): ")
    
    if response.lower() != 'yes':
        print("Exiting...")
        sys.exit(0)
        
    app = ModernPenetrationToolkit()
    app.run()