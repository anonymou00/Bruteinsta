#!/bin/bash

echo "🎮 Sega 32X Game Player Başlatılıyor... 🎮"

# Python3 ile çalıştır
if command -v python3 &> /dev/null; then
    echo "✅ Python3 bulundu, program başlatılıyor..."
    python3 sega32x_player.py
else
    echo "❌ Python3 bulunamadı!"
    echo "🔧 Kurulum için: ./install.sh"
    exit 1
fi