#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Sega 32X Player
"""

import tkinter as tk
from tkinter import messagebox

def test_gui():
    """Test GUI functionality"""
    root = tk.Tk()
    root.title("🧪 Test - Sega 32X Player")
    root.geometry("400x300")
    root.configure(bg='#1a1a2e')
    
    # Test label
    label = tk.Label(
        root,
        text="🎮 Sega 32X Player Test",
        font=('Arial', 16, 'bold'),
        fg='#ff6b35',
        bg='#1a1a2e'
    )
    label.pack(pady=50)
    
    # Test button
    def show_success():
        messagebox.showinfo("✅ Başarılı!", "GUI çalışıyor! Program hazır!")
        root.destroy()
    
    button = tk.Button(
        root,
        text="🧪 Test Et",
        command=show_success,
        bg='#4ade80',
        fg='white',
        font=('Arial', 12, 'bold'),
        relief='flat',
        padx=30,
        pady=15
    )
    button.pack(pady=20)
    
    # Status
    status = tk.Label(
        root,
        text="🎯 Test modunda çalışıyor...",
        bg='#ff6b35',
        fg='white',
        font=('Arial', 10, 'bold'),
        pady=5
    )
    status.pack(fill='x', side='bottom')
    
    root.mainloop()

if __name__ == "__main__":
    print("🧪 Test başlatılıyor...")
    test_gui()
    print("✅ Test tamamlandı!")