#!/bin/bash

echo "🚀 Sega 32X Game Player Kurulum Scripti 🚀"
echo "=============================================="

# Sistem güncellemesi
echo "📦 Sistem güncelleniyor..."
sudo apt update

# Gerekli paketlerin kurulumu
echo "🔧 Gerekli paketler kuruluyor..."
sudo apt install -y python3-tk python3-pip python3-venv

# Virtual environment oluşturma
echo "🐍 Virtual environment oluşturuluyor..."
python3 -m venv sega32x_env

# Virtual environment aktifleştirme
echo "⚡ Virtual environment aktifleştiriliyor..."
source sega32x_env/bin/activate

# Python paketlerini kurma
echo "📚 Python kütüphaneleri kuruluyor..."
pip install Pillow pygame

echo ""
echo "✅ Kurulum tamamlandı!"
echo ""
echo "🎮 Programı çalıştırmak için:"
echo "   source sega32x_env/bin/activate"
echo "   python sega32x_player.py"
echo ""
echo "🚀 Veya doğrudan:"
echo "   python3 sega32x_player.py"
echo ""
echo "🎯 Mutlu oyunlar! 🎯"