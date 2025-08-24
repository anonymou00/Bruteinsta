#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sega 32X Game Player
Modern GUI ile Sega 32X oyunlarını oynatır
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess
import threading
import json
from pathlib import Path
import platform
import webbrowser
from PIL import Image, ImageTk
import pygame
import time

class Sega32XPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 Sega 32X Game Player - ULTRA FAST! 🚀")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')
        
        # Program ayarları
        self.current_game = None
        self.game_process = None
        self.emulator_path = None
        self.games_folder = None
        
        # GUI renkleri
        self.colors = {
            'bg': '#1a1a2e',
            'fg': '#ffffff',
            'accent': '#ff6b35',
            'secondary': '#16213e',
            'success': '#4ade80',
            'warning': '#fbbf24',
            'error': '#f87171'
        }
        
        self.setup_gui()
        self.load_settings()
        self.check_emulator()
        
    def setup_gui(self):
        """Modern ve güzel GUI kurulumu"""
        # Ana stil
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['bg'])
        header_frame.pack(fill='x', padx=20, pady=20)
        
        title_label = tk.Label(
            header_frame,
            text="🎮 SEGA 32X GAME PLAYER 🎮",
            font=('Arial', 24, 'bold'),
            fg=self.colors['accent'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Ultra Hızlı Oyun Deneyimi - Çökmez, Uçar! 🚀",
            font=('Arial', 12),
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        subtitle_label.pack(pady=5)
        
        # Ana kontroller
        controls_frame = tk.Frame(self.root, bg=self.colors['bg'])
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        # Emulator seçimi
        emu_frame = tk.LabelFrame(controls_frame, text="🎯 Emulator Ayarları", 
                                 bg=self.colors['secondary'], fg=self.colors['accent'],
                                 font=('Arial', 12, 'bold'))
        emu_frame.pack(fill='x', pady=10)
        
        tk.Button(
            emu_frame,
            text="📁 Emulator Seç",
            command=self.select_emulator,
            bg=self.colors['accent'],
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=10
        ).pack(side='left', padx=10, pady=10)
        
        self.emu_label = tk.Label(
            emu_frame,
            text="Emulator seçilmedi",
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            font=('Arial', 10)
        )
        self.emu_label.pack(side='left', padx=10, pady=10)
        
        # Oyun seçimi
        game_frame = tk.LabelFrame(controls_frame, text="🎮 Oyun Seçimi", 
                                 bg=self.colors['secondary'], fg=self.colors['accent'],
                                 font=('Arial', 12, 'bold'))
        game_frame.pack(fill='x', pady=10)
        
        tk.Button(
            game_frame,
            text="🎯 Tek Oyun Seç",
            command=self.select_single_game,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=10
        ).pack(side='left', padx=10, pady=10)
        
        tk.Button(
            game_frame,
            text="📂 Klasör Seç (Çoklu)",
            command=self.select_games_folder,
            bg=self.colors['warning'],
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=10
        ).pack(side='left', padx=10, pady=10)
        
        # Oyun listesi
        list_frame = tk.LabelFrame(controls_frame, text="📋 Oyun Listesi", 
                                 bg=self.colors['secondary'], fg=self.colors['accent'],
                                 font=('Arial', 12, 'bold'))
        list_frame.pack(fill='both', expand=True, pady=10)
        
        # Scrollbar ile liste
        list_scroll = tk.Scrollbar(list_frame)
        list_scroll.pack(side='right', fill='y')
        
        self.game_listbox = tk.Listbox(
            list_frame,
            bg=self.colors['secondary'],
            fg=self.colors['fg'],
            selectbackground=self.colors['accent'],
            font=('Arial', 11),
            yscrollcommand=list_scroll.set
        )
        self.game_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        list_scroll.config(command=self.game_listbox.yview)
        
        # Oyun kontrolleri
        control_frame = tk.Frame(controls_frame, bg=self.colors['bg'])
        control_frame.pack(fill='x', pady=10)
        
        tk.Button(
            control_frame,
            text="▶️ OYNA!",
            command=self.play_game,
            bg=self.colors['success'],
            fg='white',
            font=('Arial', 14, 'bold'),
            relief='flat',
            padx=30,
            pady=15
        ).pack(side='left', padx=10)
        
        tk.Button(
            control_frame,
            text="⏹️ DURDUR",
            command=self.stop_game,
            bg=self.colors['error'],
            fg='white',
            font=('Arial', 12, 'bold'),
            relief='flat',
            padx=20,
            pady=10
        ).pack(side='left', padx=10)
        
        tk.Button(
            control_frame,
            text="🔄 Yenile",
            command=self.refresh_games,
            bg=self.colors['warning'],
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=10
        ).pack(side='left', padx=10)
        
        # Durum çubuğu
        self.status_label = tk.Label(
            self.root,
            text="🎮 Hazır! Oyun seç ve OYNA!",
            bg=self.colors['accent'],
            fg='white',
            font=('Arial', 10, 'bold'),
            pady=5
        )
        self.status_label.pack(fill='x', side='bottom')
        
        # Çift tıklama ile oyun başlatma
        self.game_listbox.bind('<Double-Button-1>', lambda e: self.play_game())
        
    def select_emulator(self):
        """Emulator dosyası seçimi"""
        try:
            file_path = filedialog.askopenfilename(
                title="🎯 Emulator Seç",
                filetypes=[
                    ("Executable files", "*.exe"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                self.emulator_path = file_path
                self.emu_label.config(text=f"✅ {os.path.basename(file_path)}")
                self.save_settings()
                self.update_status("🎯 Emulator seçildi!")
                
        except Exception as e:
            self.show_error(f"Emulator seçiminde hata: {str(e)}")
    
    def select_single_game(self):
        """Tek oyun dosyası seçimi"""
        try:
            file_path = filedialog.askopenfilename(
                title="🎮 Oyun Dosyası Seç",
                filetypes=[
                    ("32X ROM files", "*.32x"),
                    ("ROM files", "*.rom"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                self.add_game_to_list(file_path)
                self.update_status(f"🎮 Oyun eklendi: {os.path.basename(file_path)}")
                
        except Exception as e:
            self.show_error(f"Oyun seçiminde hata: {str(e)}")
    
    def select_games_folder(self):
        """Oyun klasörü seçimi"""
        try:
            folder_path = filedialog.askdirectory(title="📂 Oyun Klasörü Seç")
            
            if folder_path:
                self.games_folder = folder_path
                self.scan_games_folder()
                self.update_status(f"📂 Klasör taranıyor: {folder_path}")
                
        except Exception as e:
            self.show_error(f"Klasör seçiminde hata: {str(e)}")
    
    def scan_games_folder(self):
        """Klasördeki oyunları tara"""
        try:
            if not self.games_folder:
                return
                
            self.game_listbox.delete(0, tk.END)
            game_extensions = ['.32x', '.rom', '.bin', '.smd']
            
            for file_path in Path(self.games_folder).rglob('*'):
                if file_path.is_file() and file_path.suffix.lower() in game_extensions:
                    self.add_game_to_list(str(file_path))
                    
            self.update_status(f"📂 {self.game_listbox.size()} oyun bulundu!")
            
        except Exception as e:
            self.show_error(f"Klasör tarama hatası: {str(e)}")
    
    def add_game_to_list(self, file_path):
        """Oyun listesine oyun ekle"""
        try:
            filename = os.path.basename(file_path)
            self.game_listbox.insert(tk.END, filename)
            # Dosya yolu ile birlikte sakla
            self.game_listbox.itemconfig(tk.END, {'bg': self.colors['secondary']})
            
        except Exception as e:
            self.show_error(f"Oyun ekleme hatası: {str(e)}")
    
    def get_selected_game_path(self):
        """Seçili oyunun tam yolunu al"""
        try:
            selection = self.game_listbox.curselection()
            if not selection:
                return None
                
            selected_index = selection[0]
            selected_text = self.game_listbox.get(selected_index)
            
            # Eğer klasör taramasından geliyorsa
            if self.games_folder:
                return os.path.join(self.games_folder, selected_text)
            else:
                # Tek dosya seçiminden geliyorsa
                return selected_text
                
        except Exception as e:
            self.show_error(f"Oyun yolu alma hatası: {str(e)}")
            return None
    
    def play_game(self):
        """Oyunu başlat"""
        try:
            if not self.emulator_path:
                messagebox.showwarning("⚠️ Uyarı", "Önce emulator seçmelisin!")
                return
                
            game_path = self.get_selected_game_path()
            if not game_path:
                messagebox.showwarning("⚠️ Uyarı", "Oyun seçmelisin!")
                return
                
            if not os.path.exists(game_path):
                messagebox.showerror("❌ Hata", "Oyun dosyası bulunamadı!")
                return
            
            # Önceki oyunu durdur
            self.stop_game()
            
            # Yeni oyunu başlat
            self.current_game = game_path
            self.update_status(f"🚀 Oyun başlatılıyor: {os.path.basename(game_path)}")
            
            # Thread'de oyunu başlat
            game_thread = threading.Thread(target=self._launch_game_thread, daemon=True)
            game_thread.start()
            
        except Exception as e:
            self.show_error(f"Oyun başlatma hatası: {str(e)}")
    
    def _launch_game_thread(self):
        """Thread'de oyun başlatma"""
        try:
            # Emulator komutu
            if platform.system() == "Windows":
                cmd = [self.emulator_path, self.current_game]
            else:
                cmd = [self.emulator_path, self.current_game]
            
            # Oyunu başlat
            self.game_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if platform.system() == "Windows" else 0
            )
            
            # Ana thread'de durumu güncelle
            self.root.after(0, lambda: self.update_status(f"🎮 Oyun çalışıyor: {os.path.basename(self.current_game)}"))
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Oyun başlatma hatası: {str(e)}"))
    
    def stop_game(self):
        """Oyunu durdur"""
        try:
            if self.game_process:
                self.game_process.terminate()
                self.game_process = None
                self.current_game = None
                self.update_status("⏹️ Oyun durduruldu")
                
        except Exception as e:
            self.show_error(f"Oyun durdurma hatası: {str(e)}")
    
    def refresh_games(self):
        """Oyun listesini yenile"""
        try:
            if self.games_folder:
                self.scan_games_folder()
            else:
                self.game_listbox.delete(0, tk.END)
                
            self.update_status("🔄 Liste yenilendi")
            
        except Exception as e:
            self.show_error(f"Yenileme hatası: {str(e)}")
    
    def update_status(self, message):
        """Durum çubuğunu güncelle"""
        try:
            self.status_label.config(text=f"🎮 {message}")
            self.root.update_idletasks()
            
        except Exception as e:
            print(f"Durum güncelleme hatası: {str(e)}")
    
    def show_error(self, message):
        """Hata mesajı göster"""
        try:
            messagebox.showerror("❌ Hata", message)
            self.update_status("❌ Hata oluştu")
            
        except Exception as e:
            print(f"Hata gösterme hatası: {str(e)}")
    
    def load_settings(self):
        """Ayarları yükle"""
        try:
            settings_file = "sega32x_settings.json"
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.emulator_path = settings.get('emulator_path')
                    self.games_folder = settings.get('games_folder')
                    
                    if self.emulator_path and os.path.exists(self.emulator_path):
                        self.emu_label.config(text=f"✅ {os.path.basename(self.emulator_path)}")
                        
                    if self.games_folder and os.path.exists(self.games_folder):
                        self.scan_games_folder()
                        
        except Exception as e:
            print(f"Ayarlar yükleme hatası: {str(e)}")
    
    def save_settings(self):
        """Ayarları kaydet"""
        try:
            settings = {
                'emulator_path': self.emulator_path,
                'games_folder': self.games_folder
            }
            
            with open("sega32x_settings.json", 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Ayarlar kaydetme hatası: {str(e)}")
    
    def check_emulator(self):
        """Emulator kontrolü"""
        try:
            # Popüler emulator'ları kontrol et
            common_emulators = [
                "retroarch.exe",
                "mednafen.exe",
                "kega.exe",
                "fusion.exe"
            ]
            
            for emu in common_emulators:
                if os.path.exists(emu):
                    self.emulator_path = emu
                    self.emu_label.config(text=f"✅ {emu}")
                    self.update_status("🎯 Otomatik emulator bulundu!")
                    break
                    
        except Exception as e:
            print(f"Emulator kontrol hatası: {str(e)}")
    
    def run(self):
        """Programı çalıştır"""
        try:
            # Crash protection
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Ana döngü
            self.root.mainloop()
            
        except Exception as e:
            self.show_error(f"Program hatası: {str(e)}")
    
    def on_closing(self):
        """Program kapanırken"""
        try:
            self.stop_game()
            self.save_settings()
            self.root.destroy()
            
        except Exception as e:
            print(f"Kapanma hatası: {str(e)}")
            self.root.destroy()

def main():
    """Ana fonksiyon"""
    try:
        # Crash protection
        app = Sega32XPlayer()
        app.run()
        
    except Exception as e:
        # Son çare crash protection
        messagebox.showerror("❌ Kritik Hata", f"Program başlatılamadı: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()