import tkinter as tk
from tkinter import ttk, messagebox
import json
import threading
import time
from datetime import datetime
import random

class AzerbaijanCameraFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Azerbaycan Kamera Bulucu")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Azerbaijan cities and districts with camera data
        self.cities_data = {
            "Bakü": {
                "districts": {
                    "Nerimanov": {"cameras": 45, "locations": ["Merkez", "Azadlıq Meydanı", "28 May", "Nərimanov"]},
                    "Yasamal": {"cameras": 38, "locations": ["Yasamal", "Bakıxanov", "Əhmədli", "Badamdar"]},
                    "Sabail": {"cameras": 42, "locations": ["İçərişəhər", "Sahil", "Səbail", "Qobustan"]},
                    "Binəqədi": {"cameras": 35, "locations": ["Binəqədi", "Xırdalan", "Mərdəkan", "Bilgəh"]},
                    "Xətai": {"cameras": 40, "locations": ["Xətai", "Ələt", "Qaradağ", "Lökbatan"]},
                    "Suraxanı": {"cameras": 33, "locations": ["Suraxanı", "Biləcəri", "Qala", "Şüvəlan"]},
                    "Nəsimi": {"cameras": 37, "locations": ["Nəsimi", "Bakıxanov", "Xocəsən", "Qobu"]},
                    "Qaradağ": {"cameras": 28, "locations": ["Qaradağ", "Ələt", "Lökbatan", "Sahil"]},
                    "Pirallahı": {"cameras": 15, "locations": ["Pirallahı", "Nardaran", "Bilgəh", "Mərdəkan"]},
                    "Xəzər": {"cameras": 22, "locations": ["Xəzər", "Buzovna", "Mərdəkan", "Şüvəlan"]}
                }
            },
            "Gəncə": {
                "districts": {
                    "Kəpəz": {"cameras": 25, "locations": ["Kəpəz", "Gəncə Mərkəz", "Nizami", "Şah İsmayıl Xətai"]},
                    "Nizami": {"cameras": 20, "locations": ["Nizami", "Gəncə Mərkəz", "Kəpəz", "Şah İsmayıl Xətai"]}
                }
            },
            "Sumqayıt": {
                "districts": {
                    "Mərkəz": {"cameras": 18, "locations": ["Sumqayıt Mərkəz", "Hacı Zeynalabdin", "Əhmədli", "Yeni Sumqayıt"]},
                    "Hacı Zeynalabdin": {"cameras": 15, "locations": ["Hacı Zeynalabdin", "Əhmədli", "Yeni Sumqayıt", "Mərkəz"]}
                }
            },
            "Mingəçevir": {
                "districts": {
                    "Mərkəz": {"cameras": 12, "locations": ["Mingəçevir Mərkəz", "Yeni Mingəçevir", "Kür", "Səngər"]}
                }
            },
            "Şəki": {
                "districts": {
                    "Mərkəz": {"cameras": 10, "locations": ["Şəki Mərkəz", "Yuxarı Baş", "Aşağı Baş", "Qarabağlar"]}
                }
            },
            "Şamaxı": {
                "districts": {
                    "Mərkəz": {"cameras": 8, "locations": ["Şamaxı Mərkəz", "Qobustan", "Pirqulu", "Mədrəsə"]}
                }
            },
            "Quba": {
                "districts": {
                    "Mərkəz": {"cameras": 9, "locations": ["Quba Mərkəz", "Qırmızı Qəsəbə", "Qonaqkənd", "İspik"]}
                }
            },
            "Qusar": {
                "districts": {
                    "Mərkəz": {"cameras": 7, "locations": ["Qusar Mərkəz", "Qubaçı", "Qudyal", "Samur"]}
                }
            },
            "Xaçmaz": {
                "districts": {
                    "Mərkəz": {"cameras": 6, "locations": ["Xaçmaz Mərkəz", "Qubaçı", "Qudyal", "Samur"]}
                }
            },
            "Lənkəran": {
                "districts": {
                    "Mərkəz": {"cameras": 11, "locations": ["Lənkəran Mərkəz", "Şirvan", "Astara", "Masallı"]}
                }
            },
            "Astara": {
                "districts": {
                    "Mərkəz": {"cameras": 5, "locations": ["Astara Mərkəz", "Lənkəran", "Masallı", "Şirvan"]}
                }
            },
            "Masallı": {
                "districts": {
                    "Mərkəz": {"cameras": 6, "locations": ["Masallı Mərkəz", "Lənkəran", "Astara", "Şirvan"]}
                }
            },
            "Şirvan": {
                "districts": {
                    "Mərkəz": {"cameras": 8, "locations": ["Şirvan Mərkəz", "Lənkəran", "Masallı", "Astara"]}
                }
            },
            "Yevlax": {
                "districts": {
                    "Mərkəz": {"cameras": 7, "locations": ["Yevlax Mərkəz", "Mingəçevir", "Ağdaş", "Göyçay"]}
                }
            },
            "Ağdaş": {
                "districts": {
                    "Mərkəz": {"cameras": 5, "locations": ["Ağdaş Mərkəz", "Yevlax", "Göyçay", "Kürdəmir"]}
                }
            },
            "Göyçay": {
                "districts": {
                    "Mərkəz": {"cameras": 6, "locations": ["Göyçay Mərkəz", "Ağdaş", "Yevlax", "Kürdəmir"]}
                }
            },
            "Kürdəmir": {
                "districts": {
                    "Mərkəz": {"cameras": 4, "locations": ["Kürdəmir Mərkəz", "Ağdaş", "Göyçay", "Yevlax"]}
                }
            },
            "Ucar": {
                "districts": {
                    "Mərkəz": {"cameras": 5, "locations": ["Ucar Mərkəz", "Ağdaş", "Göyçay", "Kürdəmir"]}
                }
            },
            "Zərdab": {
                "districts": {
                    "Mərkəz": {"cameras": 3, "locations": ["Zərdab Mərkəz", "Ucar", "Ağdaş", "Göyçay"]}
                }
            },
            "Bərdə": {
                "districts": {
                    "Mərkəz": {"cameras": 7, "locations": ["Bərdə Mərkəz", "Tərtər", "Ağcabədi", "Ağdam"]}
                }
            },
            "Tərtər": {
                "districts": {
                    "Mərkəz": {"cameras": 6, "locations": ["Tərtər Mərkəz", "Bərdə", "Ağcabədi", "Ağdam"]}
                }
            },
            "Ağcabədi": {
                "districts": {
                    "Mərkəz": {"cameras": 5, "locations": ["Ağcabədi Mərkəz", "Bərdə", "Tərtər", "Ağdam"]}
                }
            },
            "Ağdam": {
                "districts": {
                    "Mərkəz": {"cameras": 4, "locations": ["Ağdam Mərkəz", "Bərdə", "Tərtər", "Ağcabədi"]}
                }
            },
            "Füzuli": {
                "districts": {
                    "Mərkəz": {"cameras": 3, "locations": ["Füzuli Mərkəz", "Xocavənd", "Cəbrayıl", "Qubadlı"]}
                }
            },
            "Xocavənd": {
                "districts": {
                    "Mərkəz": {"cameras": 2, "locations": ["Xocavənd Mərkəz", "Füzuli", "Cəbrayıl", "Qubadlı"]}
                }
            },
            "Cəbrayıl": {
                "districts": {
                    "Mərkəz": {"cameras": 2, "locations": ["Cəbrayıl Mərkəz", "Füzuli", "Xocavənd", "Qubadlı"]}
                }
            },
            "Qubadlı": {
                "districts": {
                    "Mərkəz": {"cameras": 2, "locations": ["Qubadlı Mərkəz", "Füzuli", "Xocavənd", "Cəbrayıl"]}
                }
            },
            "Zəngilan": {
                "districts": {
                    "Mərkəz": {"cameras": 1, "locations": ["Zəngilan Mərkəz", "Qubadlı", "Cəbrayıl", "Füzuli"]}
                }
            },
            "Laçın": {
                "districts": {
                    "Mərkəz": {"cameras": 2, "locations": ["Laçın Mərkəz", "Qubadlı", "Zəngilan", "Kəlbəcər"]}
                }
            },
            "Kəlbəcər": {
                "districts": {
                    "Mərkəz": {"cameras": 2, "locations": ["Kəlbəcər Mərkəz", "Laçın", "Qubadlı", "Zəngilan"]}
                }
            },
            "Şuşa": {
                "districts": {
                    "Mərkəz": {"cameras": 3, "locations": ["Şuşa Mərkəz", "Xankəndi", "Ağdam", "Kəlbəcər"]}
                }
            },
            "Xankəndi": {
                "districts": {
                    "Mərkəz": {"cameras": 4, "locations": ["Xankəndi Mərkəz", "Şuşa", "Ağdam", "Kəlbəcər"]}
                }
            },
            "Xocalı": {
                "districts": {
                    "Mərkəz": {"cameras": 2, "locations": ["Xocalı Mərkəz", "Xankəndi", "Şuşa", "Ağdam"]}
                }
            },
            "Ağdərə": {
                "districts": {
                    "Mərkəz": {"cameras": 1, "locations": ["Ağdərə Mərkəz", "Xankəndi", "Xocalı", "Şuşa"]}
                }
            }
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Azerbaycan Kamera Bulucu", 
                              font=('Arial', 24, 'bold'), 
                              fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Search frame
        search_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        # City selection
        city_frame = tk.Frame(search_frame, bg='#34495e')
        city_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(city_frame, text="Şəhər Seçin:", 
                font=('Arial', 12, 'bold'), 
                fg='#ecf0f1', bg='#34495e').pack(anchor=tk.W)
        
        self.city_var = tk.StringVar()
        self.city_combo = ttk.Combobox(city_frame, textvariable=self.city_var, 
                                      font=('Arial', 11), state='readonly')
        self.city_combo['values'] = list(self.cities_data.keys())
        self.city_combo.pack(fill=tk.X, pady=(5, 0))
        self.city_combo.bind('<<ComboboxSelected>>', self.on_city_selected)
        
        # District selection
        district_frame = tk.Frame(search_frame, bg='#34495e')
        district_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tk.Label(district_frame, text="Rayon Seçin:", 
                font=('Arial', 12, 'bold'), 
                fg='#ecf0f1', bg='#34495e').pack(anchor=tk.W)
        
        self.district_var = tk.StringVar()
        self.district_combo = ttk.Combobox(district_frame, textvariable=self.district_var, 
                                          font=('Arial', 11), state='readonly')
        self.district_combo.pack(fill=tk.X, pady=(5, 0))
        self.district_combo.bind('<<ComboboxSelected>>', self.on_district_selected)
        
        # Search button
        button_frame = tk.Frame(search_frame, bg='#34495e')
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.search_btn = tk.Button(button_frame, text="Kamera Ara", 
                                   command=self.search_cameras,
                                   font=('Arial', 12, 'bold'),
                                   bg='#3498db', fg='white',
                                   relief=tk.FLAT, padx=30, pady=10)
        self.search_btn.pack(side=tk.LEFT)
        
        self.clear_btn = tk.Button(button_frame, text="Təmizlə", 
                                  command=self.clear_results,
                                  font=('Arial', 12, 'bold'),
                                  bg='#e74c3c', fg='white',
                                  relief=tk.FLAT, padx=30, pady=10)
        self.clear_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Results frame
        results_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results title
        results_title = tk.Label(results_frame, text="Kamera Nəticələri", 
                                font=('Arial', 16, 'bold'), 
                                fg='#ecf0f1', bg='#34495e')
        results_title.pack(pady=20)
        
        # Results text area
        self.results_text = tk.Text(results_frame, font=('Arial', 11), 
                                   bg='#ecf0f1', fg='#2c3e50',
                                   wrap=tk.WORD, relief=tk.FLAT)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Scrollbar for results
        scrollbar = tk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır - Şəhər və rayon seçin")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                             font=('Arial', 10), 
                             fg='#bdc3c7', bg='#2c3e50')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
    def on_city_selected(self, event=None):
        selected_city = self.city_var.get()
        if selected_city in self.cities_data:
            districts = list(self.cities_data[selected_city]['districts'].keys())
            self.district_combo['values'] = districts
            self.district_combo.set('')
            self.status_var.set(f"{selected_city} şəhəri seçildi - {len(districts)} rayon mövcuddur")
            
    def on_district_selected(self, event=None):
        selected_district = self.district_var.get()
        if selected_district:
            self.status_var.set(f"Rayon seçildi: {selected_district} - Aramağa hazır")
            
    def search_cameras(self):
        city = self.city_var.get()
        district = self.district_var.get()
        
        if not city or not district:
            messagebox.showwarning("Xəbərdarlıq", "Zəhmət olmasa şəhər və rayon seçin!")
            return
            
        # Simulate fast search
        self.status_var.set("Axtarılır...")
        self.search_btn.config(state=tk.DISABLED)
        
        # Run search in separate thread for responsiveness
        threading.Thread(target=self.perform_search, args=(city, district), daemon=True).start()
        
    def perform_search(self, city, district):
        try:
            # Simulate fast search delay
            time.sleep(0.1)
            
            camera_data = self.cities_data[city]['districts'][district]
            camera_count = camera_data['cameras']
            locations = camera_data['locations']
            
            # Generate detailed camera information
            camera_details = []
            for i in range(camera_count):
                location = random.choice(locations)
                camera_type = random.choice(['HD', '4K', 'IP', 'PTZ', 'Dome'])
                status = random.choice(['Aktiv', 'Aktiv', 'Aktiv', 'Təmir', 'Offline'])
                
                camera_details.append({
                    'id': f"KAM-{city[:3].upper()}-{district[:3].upper()}-{i+1:03d}",
                    'location': location,
                    'type': camera_type,
                    'status': status,
                    'coordinates': f"{random.uniform(40.0, 42.0):.6f}, {random.uniform(44.0, 51.0):.6f}"
                })
            
            # Update UI in main thread
            self.root.after(0, self.display_results, city, district, camera_details)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Xəta", f"Axtarış zamanı xəta baş verdi: {str(e)}"))
            self.root.after(0, lambda: self.search_btn.config(state=tk.NORMAL))
            
    def display_results(self, city, district, camera_details):
        self.results_text.delete(1.0, tk.END)
        
        # Header
        header = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           KAMERA AXTARIŞ NƏTICƏSI                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Şəhər: {city:<60} ║
║ Rayon: {district:<60} ║
║ Ümumi Kamera Sayı: {len(camera_details):<50} ║
║ Axtarış Tarixi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S'):<45} ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""
        self.results_text.insert(tk.END, header)
        
        # Camera details
        for i, camera in enumerate(camera_details, 1):
            status_color = "🟢" if camera['status'] == 'Aktiv' else "🔴" if camera['status'] == 'Offline' else "🟡"
            
            camera_info = f"""
┌─ Kamera #{i:03d} ──────────────────────────────────────────────────────────────┐
│ ID: {camera['id']:<65} │
│ Yer: {camera['location']:<65} │
│ Növ: {camera['type']:<65} │
│ Status: {status_color} {camera['status']:<60} │
│ Koordinatlar: {camera['coordinates']:<55} │
└─────────────────────────────────────────────────────────────────────────────────┘
"""
            self.results_text.insert(tk.END, camera_info)
            
        # Summary
        active_cameras = sum(1 for cam in camera_details if cam['status'] == 'Aktiv')
        offline_cameras = sum(1 for cam in camera_details if cam['status'] == 'Offline')
        repair_cameras = sum(1 for cam in camera_details if cam['status'] == 'Təmir')
        
        summary = f"""

╔══════════════════════════════════════════════════════════════════════════════╗
║                              ÜMUMİ MƏLUMAT                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 🟢 Aktiv Kameralar: {active_cameras:<50} ║
║ 🔴 Offline Kameralar: {offline_cameras:<47} ║
║ 🟡 Təmir Kameralar: {repair_cameras:<48} ║
║ 📊 Ümumi Kamera Sayı: {len(camera_details):<47} ║
╚══════════════════════════════════════════════════════════════════════════════╝

Axtarış tamamlandı! {len(camera_details)} kamera tapıldı.
"""
        self.results_text.insert(tk.END, summary)
        
        self.status_var.set(f"Axtarış tamamlandı - {city}, {district}: {len(camera_details)} kamera tapıldı")
        self.search_btn.config(state=tk.NORMAL)
        
    def clear_results(self):
        self.results_text.delete(1.0, tk.END)
        self.city_var.set('')
        self.district_var.set('')
        self.district_combo['values'] = []
        self.status_var.set("Hazır - Şəhər və rayon seçin")

def main():
    root = tk.Tk()
    app = AzerbaijanCameraFinder(root)
    
    # Configure modern theme
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure colors for modern look
    style.configure('TCombobox', 
                   fieldbackground='#ecf0f1',
                   background='#3498db',
                   foreground='#2c3e50',
                   arrowcolor='#2c3e50')
    
    root.mainloop()

if __name__ == "__main__":
    main()