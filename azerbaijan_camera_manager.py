import tkinter as tk
from tkinter import ttk, messagebox
import json
import threading
import time
from datetime import datetime
import socket
import ipaddress

class AzerbaijanCameraManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Azərbaycan Kamera İdarəetmə Sistemi")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Azerbaijan cities and districts data
        self.cities_data = {
            "Bakı": {
                "districts": ["Binəqədi", "Qaradağ", "Xətai", "Xəzər", "Nərimanov", "Nəsiyyə", "Pirallahı", "Sabunçu", "Səbail", "Suraxanı", "Yasamal"],
                "cameras": [
                    {"name": "Bakı Mərkəz", "ip": "192.168.1.100", "port": 8080, "status": "active"},
                    {"name": "Dənizkənarı", "ip": "192.168.1.101", "port": 8081, "status": "active"},
                    {"name": "Fəvvarələr", "ip": "192.168.1.102", "port": 8082, "status": "active"},
                    {"name": "28 May", "ip": "192.168.1.103", "port": 8083, "status": "active"},
                    {"name": "Nərimanov", "ip": "192.168.1.104", "port": 8084, "status": "active"}
                ]
            },
            "Gəncə": {
                "districts": ["Kəpəz", "Nizami"],
                "cameras": [
                    {"name": "Gəncə Mərkəz", "ip": "192.168.2.100", "port": 8080, "status": "active"},
                    {"name": "Şah Abbas", "ip": "192.168.2.101", "port": 8081, "status": "active"},
                    {"name": "Nizami", "ip": "192.168.2.102", "port": 8082, "status": "active"}
                ]
            },
            "Sumqayıt": {
                "districts": ["Bayıl", "Cəfər Cabbarlı", "Əhmədli"],
                "cameras": [
                    {"name": "Sumqayıt Mərkəz", "ip": "192.168.3.100", "port": 8080, "status": "active"},
                    {"name": "Bayıl", "ip": "192.168.3.101", "port": 8081, "status": "active"},
                    {"name": "Əhmədli", "ip": "192.168.3.102", "port": 8082, "status": "active"}
                ]
            },
            "Mingəçevir": {
                "districts": ["Mingəçevir"],
                "cameras": [
                    {"name": "Mingəçevir Mərkəz", "ip": "192.168.4.100", "port": 8080, "status": "active"},
                    {"name": "Kür Sahili", "ip": "192.168.4.101", "port": 8081, "status": "active"}
                ]
            },
            "Şəki": {
                "districts": ["Şəki"],
                "cameras": [
                    {"name": "Şəki Mərkəz", "ip": "192.168.5.100", "port": 8080, "status": "active"},
                    {"name": "Şəki Qalası", "ip": "192.168.5.101", "port": 8081, "status": "active"}
                ]
            },
            "Quba": {
                "districts": ["Quba"],
                "cameras": [
                    {"name": "Quba Mərkəz", "ip": "192.168.6.100", "port": 8080, "status": "active"},
                    {"name": "Quba Bazar", "ip": "192.168.6.101", "port": 8081, "status": "active"}
                ]
            },
            "Lənkəran": {
                "districts": ["Lənkəran"],
                "cameras": [
                    {"name": "Lənkəran Mərkəz", "ip": "192.168.7.100", "port": 8080, "status": "active"},
                    {"name": "Lənkəran Sahil", "ip": "192.168.7.101", "port": 8081, "status": "active"}
                ]
            },
            "Şirvan": {
                "districts": ["Şirvan"],
                "cameras": [
                    {"name": "Şirvan Mərkəz", "ip": "192.168.8.100", "port": 8080, "status": "active"},
                    {"name": "Şirvan Sənaye", "ip": "192.168.8.101", "port": 8081, "status": "active"}
                ]
            },
            "Naxçıvan": {
                "districts": ["Naxçıvan"],
                "cameras": [
                    {"name": "Naxçıvan Mərkəz", "ip": "192.168.9.100", "port": 8080, "status": "active"},
                    {"name": "Naxçıvan Qalası", "ip": "192.168.9.101", "port": 8081, "status": "active"}
                ]
            },
            "Xankəndi": {
                "districts": ["Xankəndi"],
                "cameras": [
                    {"name": "Xankəndi Mərkəz", "ip": "192.168.10.100", "port": 8080, "status": "active"},
                    {"name": "Xankəndi Bazar", "ip": "192.168.10.101", "port": 8081, "status": "active"}
                ]
            }
        }
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Azərbaycan Kamera İdarəetmə Sistemi", 
                              font=('Arial', 24, 'bold'), fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # City selection
        city_frame = tk.Frame(control_frame, bg='#34495e')
        city_frame.pack(side=tk.LEFT, padx=20, pady=20)
        
        tk.Label(city_frame, text="Şəhər seçin:", font=('Arial', 12, 'bold'), 
                fg='#ecf0f1', bg='#34495e').pack(anchor=tk.W)
        
        self.city_var = tk.StringVar()
        self.city_combo = ttk.Combobox(city_frame, textvariable=self.city_var, 
                                      font=('Arial', 11), width=20, state='readonly')
        self.city_combo.pack(pady=(5, 0))
        self.city_combo.bind('<<ComboboxSelected>>', self.on_city_selected)
        
        # District selection
        district_frame = tk.Frame(control_frame, bg='#34495e')
        district_frame.pack(side=tk.LEFT, padx=20, pady=20)
        
        tk.Label(district_frame, text="Rayon seçin:", font=('Arial', 12, 'bold'), 
                fg='#ecf0f1', bg='#34495e').pack(anchor=tk.W)
        
        self.district_var = tk.StringVar()
        self.district_combo = ttk.Combobox(district_frame, textvariable=self.district_var, 
                                          font=('Arial', 11), width=20, state='readonly')
        self.district_combo.pack(pady=(5, 0))
        self.district_combo.bind('<<ComboboxSelected>>', self.on_district_selected)
        
        # Search button
        search_frame = tk.Frame(control_frame, bg='#34495e')
        search_frame.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.search_btn = tk.Button(search_frame, text="Kamera Axtar", 
                                   command=self.search_cameras,
                                   font=('Arial', 12, 'bold'), 
                                   bg='#3498db', fg='white',
                                   relief=tk.FLAT, padx=20, pady=10)
        self.search_btn.pack(pady=(25, 0))
        
        # Status frame
        status_frame = tk.Frame(control_frame, bg='#34495e')
        status_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.status_label = tk.Label(status_frame, text="Status: Hazır", 
                                    font=('Arial', 10), fg='#2ecc71', bg='#34495e')
        self.status_label.pack()
        
        # Results area
        results_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results title
        results_title = tk.Label(results_frame, text="Kamera Nəticələri", 
                                font=('Arial', 16, 'bold'), fg='#ecf0f1', bg='#34495e')
        results_title.pack(pady=10)
        
        # Treeview for results
        self.tree = ttk.Treeview(results_frame, columns=('name', 'ip', 'port', 'status', 'city', 'district'), 
                                 show='headings', height=15)
        
        # Configure columns
        self.tree.heading('name', text='Kamera Adı')
        self.tree.heading('ip', text='IP Ünvanı')
        self.tree.heading('port', text='Port')
        self.tree.heading('status', text='Status')
        self.tree.heading('city', text='Şəhər')
        self.tree.heading('district', text='Rayon')
        
        self.tree.column('name', width=200)
        self.tree.column('ip', width=150)
        self.tree.column('port', width=100)
        self.tree.column('status', width=100)
        self.tree.column('city', width=150)
        self.tree.column('district', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Right click menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="IP/Port Kopyala", command=self.copy_ip_port)
        self.context_menu.add_command(label="Kamera Məlumatları", command=self.show_camera_details)
        
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # Statistics frame
        stats_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.stats_label = tk.Label(stats_frame, text="Ümumi Kamera Sayı: 0 | Aktiv: 0 | Deaktiv: 0", 
                                   font=('Arial', 12), fg='#ecf0f1', bg='#34495e')
        self.stats_label.pack(pady=10)
        
    def load_data(self):
        """Load cities into combobox"""
        cities = list(self.cities_data.keys())
        self.city_combo['values'] = cities
        if cities:
            self.city_combo.set(cities[0])
            self.on_city_selected()
            
    def on_city_selected(self, event=None):
        """Handle city selection"""
        selected_city = self.city_var.get()
        if selected_city in self.cities_data:
            districts = self.cities_data[selected_city]['districts']
            self.district_combo['values'] = districts
            if districts:
                self.district_combo.set(districts[0])
                
    def on_district_selected(self, event=None):
        """Handle district selection"""
        pass
        
    def search_cameras(self):
        """Search for cameras based on selection"""
        self.status_label.config(text="Status: Axtarılır...", fg='#f39c12')
        self.root.update()
        
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        selected_city = self.city_var.get()
        selected_district = self.district_var.get()
        
        if not selected_city:
            messagebox.showwarning("Xəbərdarlıq", "Zəhmət olmasa şəhər seçin!")
            return
            
        # Simulate fast search
        def search_thread():
            time.sleep(0.1)  # Simulate processing time
            
            cameras_found = []
            
            if selected_district:
                # Search in specific district
                if selected_city in self.cities_data:
                    cameras = self.cities_data[selected_city]['cameras']
                    for camera in cameras:
                        cameras_found.append({
                            'name': camera['name'],
                            'ip': camera['ip'],
                            'port': camera['port'],
                            'status': camera['status'],
                            'city': selected_city,
                            'district': selected_district
                        })
            else:
                # Search in entire city
                if selected_city in self.cities_data:
                    cameras = self.cities_data[selected_city]['cameras']
                    for camera in cameras:
                        cameras_found.append({
                            'name': camera['name'],
                            'ip': camera['ip'],
                            'port': camera['port'],
                            'status': camera['status'],
                            'city': selected_city,
                            'district': selected_city
                        })
            
            # Update UI in main thread
            self.root.after(0, self.update_results, cameras_found)
            
        threading.Thread(target=search_thread, daemon=True).start()
        
    def update_results(self, cameras):
        """Update results in treeview"""
        for camera in cameras:
            status_color = '#2ecc71' if camera['status'] == 'active' else '#e74c3c'
            
            item = self.tree.insert('', 'end', values=(
                camera['name'],
                camera['ip'],
                camera['port'],
                camera['status'],
                camera['city'],
                camera['district']
            ))
            
            # Color code based on status
            if camera['status'] == 'active':
                self.tree.tag_configure('active', foreground='#2ecc71')
                self.tree.item(item, tags=('active',))
            else:
                self.tree.tag_configure('inactive', foreground='#e74c3c')
                self.tree.item(item, tags=('inactive',))
        
        # Update statistics
        total_cameras = len(cameras)
        active_cameras = len([c for c in cameras if c['status'] == 'active'])
        inactive_cameras = total_cameras - active_cameras
        
        self.stats_label.config(text=f"Ümumi Kamera Sayı: {total_cameras} | Aktiv: {active_cameras} | Deaktiv: {inactive_cameras}")
        self.status_label.config(text=f"Status: {total_cameras} kamera tapıldı", fg='#2ecc71')
        
    def show_context_menu(self, event):
        """Show right-click context menu"""
        try:
            self.tree.selection_set(self.tree.identify_row(event.y))
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
            
    def copy_ip_port(self):
        """Copy IP and port to clipboard"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            ip = item['values'][1]
            port = item['values'][2]
            clipboard_text = f"{ip}:{port}"
            self.root.clipboard_clear()
            self.root.clipboard_append(clipboard_text)
            messagebox.showinfo("Məlumat", f"IP və Port kopyalandı: {clipboard_text}")
            
    def show_camera_details(self):
        """Show detailed camera information"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            details_window = tk.Toplevel(self.root)
            details_window.title("Kamera Məlumatları")
            details_window.geometry("400x300")
            details_window.configure(bg='#2c3e50')
            
            details_text = f"""
Kamera Adı: {values[0]}
IP Ünvanı: {values[1]}
Port: {values[2]}
Status: {values[3]}
Şəhər: {values[4]}
Rayon: {values[5]}

Əlavə Məlumatlar:
- Kamera Tipi: IP Kamera
- Protokol: RTSP
- Həll: 1920x1080
- FPS: 30
- Kodlaşdırma: H.264
- Audio: Dəstəklənir
- IR: Aktiv
- PoE: Dəstəklənir
            """
            
            text_widget = tk.Text(details_window, wrap=tk.WORD, font=('Arial', 11),
                                 bg='#34495e', fg='#ecf0f1', relief=tk.FLAT)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            text_widget.insert(tk.END, details_text)
            text_widget.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    
    # Configure modern theme
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure colors
    style.configure('Treeview', background='#34495e', foreground='#ecf0f1', 
                   fieldbackground='#34495e', rowheight=25)
    style.configure('Treeview.Heading', background='#2c3e50', foreground='#ecf0f1')
    style.map('Treeview', background=[('selected', '#3498db')])
    
    style.configure('TCombobox', background='#34495e', foreground='#ecf0f1')
    
    app = AzerbaijanCameraManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()