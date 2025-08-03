import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import time
import requests
import json
import os
from datetime import datetime
import queue

class SMSSender:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Toplu SMS Gönderici")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Değişkenler
        self.phone_numbers = []
        self.message = ""
        self.is_sending = False
        self.sent_count = 0
        self.failed_count = 0
        self.total_count = 0
        
        # SMS API ayarları (örnek)
        self.api_url = "https://api.example.com/sms/send"
        self.api_key = "your_api_key_here"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Ana başlık
        title_label = tk.Label(
            self.root, 
            text="Toplu SMS Gönderici", 
            font=("Arial", 20, "bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=20)
        
        # Dosya seçimi frame
        file_frame = tk.Frame(self.root, bg='#f0f0f0')
        file_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            file_frame, 
            text="Numara Dosyası:", 
            font=("Arial", 12),
            bg='#f0f0f0'
        ).pack(side='left')
        
        self.file_path_var = tk.StringVar()
        self.file_entry = tk.Entry(
            file_frame, 
            textvariable=self.file_path_var,
            width=50,
            font=("Arial", 10)
        )
        self.file_entry.pack(side='left', padx=10)
        
        tk.Button(
            file_frame,
            text="Dosya Seç",
            command=self.select_file,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 10, "bold"),
            relief='flat',
            padx=20
        ).pack(side='left')
        
        # Mesaj frame
        message_frame = tk.Frame(self.root, bg='#f0f0f0')
        message_frame.pack(pady=10, padx=20, fill='x')
        
        tk.Label(
            message_frame,
            text="Mesaj:",
            font=("Arial", 12),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        self.message_text = scrolledtext.ScrolledText(
            message_frame,
            height=4,
            font=("Arial", 10),
            wrap='word'
        )
        self.message_text.pack(fill='x', pady=5)
        
        # Kontrol frame
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(pady=10, padx=20, fill='x')
        
        # Hız ayarı
        speed_frame = tk.Frame(control_frame, bg='#f0f0f0')
        speed_frame.pack(side='left', padx=20)
        
        tk.Label(
            speed_frame,
            text="Gönderim Hızı (ms):",
            font=("Arial", 10),
            bg='#f0f0f0'
        ).pack()
        
        self.speed_var = tk.StringVar(value="100")
        speed_spinbox = tk.Spinbox(
            speed_frame,
            from_=50,
            to=1000,
            increment=50,
            textvariable=self.speed_var,
            width=10,
            font=("Arial", 10)
        )
        speed_spinbox.pack()
        
        # Butonlar
        button_frame = tk.Frame(control_frame, bg='#f0f0f0')
        button_frame.pack(side='right')
        
        self.start_button = tk.Button(
            button_frame,
            text="Gönderimi Başlat",
            command=self.start_sending,
            bg='#2196F3',
            fg='white',
            font=("Arial", 12, "bold"),
            relief='flat',
            padx=30,
            pady=10
        )
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = tk.Button(
            button_frame,
            text="Durdur",
            command=self.stop_sending,
            bg='#f44336',
            fg='white',
            font=("Arial", 12, "bold"),
            relief='flat',
            padx=30,
            pady=10,
            state='disabled'
        )
        self.stop_button.pack(side='left', padx=5)
        
        # İstatistikler frame
        stats_frame = tk.Frame(self.root, bg='#f0f0f0')
        stats_frame.pack(pady=10, padx=20, fill='x')
        
        # İstatistik etiketleri
        self.total_label = tk.Label(
            stats_frame,
            text="Toplam: 0",
            font=("Arial", 12),
            bg='#f0f0f0'
        )
        self.total_label.pack(side='left', padx=20)
        
        self.sent_label = tk.Label(
            stats_frame,
            text="Gönderilen: 0",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#4CAF50'
        )
        self.sent_label.pack(side='left', padx=20)
        
        self.failed_label = tk.Label(
            stats_frame,
            text="Başarısız: 0",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#f44336'
        )
        self.failed_label.pack(side='left', padx=20)
        
        # İlerleme çubuğu
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.root,
            variable=self.progress_var,
            maximum=100,
            length=700
        )
        self.progress_bar.pack(pady=10)
        
        # Log frame
        log_frame = tk.Frame(self.root, bg='#f0f0f0')
        log_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        tk.Label(
            log_frame,
            text="Gönderim Logları:",
            font=("Arial", 12),
            bg='#f0f0f0'
        ).pack(anchor='w')
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=("Consolas", 9),
            bg='#2b2b2b',
            fg='#ffffff'
        )
        self.log_text.pack(fill='both', expand=True)
        
    def select_file(self):
        filename = filedialog.askopenfilename(
            title="Numara dosyasını seçin",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
            self.load_phone_numbers()
    
    def load_phone_numbers(self):
        try:
            with open(self.file_path_var.get(), 'r', encoding='utf-8') as file:
                numbers = file.read().splitlines()
                # Boş satırları ve boşlukları temizle
                self.phone_numbers = [num.strip() for num in numbers if num.strip()]
                self.total_count = len(self.phone_numbers)
                self.total_label.config(text=f"Toplam: {self.total_count}")
                self.log_message(f"{self.total_count} numara yüklendi")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya okuma hatası: {str(e)}")
    
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def send_sms(self, phone_number, message):
        """SMS gönderme fonksiyonu - API entegrasyonu burada yapılacak"""
        try:
            # Bu kısım gerçek SMS API'si ile değiştirilmeli
            # Örnek API çağrısı:
            """
            payload = {
                'phone': phone_number,
                'message': message,
                'api_key': self.api_key
            }
            response = requests.post(self.api_url, json=payload, timeout=10)
            return response.status_code == 200
            """
            
            # Simülasyon için rastgele başarı/başarısızlık
            import random
            time.sleep(0.1)  # API çağrısı simülasyonu
            return random.choice([True, True, True, False])  # %75 başarı oranı
            
        except Exception as e:
            self.log_message(f"Hata: {phone_number} - {str(e)}")
            return False
    
    def start_sending(self):
        if not self.phone_numbers:
            messagebox.showwarning("Uyarı", "Lütfen önce numara dosyası seçin!")
            return
        
        if not self.message_text.get("1.0", tk.END).strip():
            messagebox.showwarning("Uyarı", "Lütfen mesaj yazın!")
            return
        
        self.message = self.message_text.get("1.0", tk.END).strip()
        self.is_sending = True
        self.sent_count = 0
        self.failed_count = 0
        
        # UI güncelleme
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.progress_var.set(0)
        
        # Gönderim thread'ini başlat
        self.send_thread = threading.Thread(target=self.send_messages)
        self.send_thread.daemon = True
        self.send_thread.start()
    
    def send_messages(self):
        speed = int(self.speed_var.get())
        
        for i, phone_number in enumerate(self.phone_numbers):
            if not self.is_sending:
                break
            
            # SMS gönder
            success = self.send_sms(phone_number, self.message)
            
            if success:
                self.sent_count += 1
                self.log_message(f"✓ {phone_number} - Başarılı")
            else:
                self.failed_count += 1
                self.log_message(f"✗ {phone_number} - Başarısız")
            
            # İstatistikleri güncelle
            self.sent_label.config(text=f"Gönderilen: {self.sent_count}")
            self.failed_label.config(text=f"Başarısız: {self.failed_count}")
            
            # İlerleme çubuğunu güncelle
            progress = ((i + 1) / self.total_count) * 100
            self.progress_var.set(progress)
            
            # Hız kontrolü
            time.sleep(speed / 1000)
        
        # Gönderim tamamlandı
        self.sending_completed()
    
    def stop_sending(self):
        self.is_sending = False
        self.log_message("Gönderim durduruldu")
        self.sending_completed()
    
    def sending_completed(self):
        self.is_sending = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        
        # Özet raporu
        summary = f"\nGönderim tamamlandı!\nToplam: {self.total_count}\nBaşarılı: {self.sent_count}\nBaşarısız: {self.failed_count}"
        self.log_message(summary)
        
        if self.sent_count > 0:
            messagebox.showinfo("Tamamlandı", f"Gönderim tamamlandı!\nBaşarılı: {self.sent_count}\nBaşarısız: {self.failed_count}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SMSSender()
    app.run()