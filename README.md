# 🚀 Sega 32X Game Player - ULTRA FAST! 🚀

Modern ve güzel GUI'ye sahip Sega 32X oyun oynatıcısı. Program çökmeyecek ve havada uçacak gibi hızlı olacak!

## ✨ Özellikler

- 🎮 **Modern GUI**: Güzel ve kullanıcı dostu arayüz
- 📁 **Dosya Seçici**: File Explorer ile kolay oyun seçimi
- 📂 **Klasör Tarama**: Tüm klasördeki oyunları otomatik bulma
- 🚀 **Ultra Hızlı**: Thread'ler ile performans optimizasyonu
- 💾 **Ayarları Kaydetme**: Emulator ve klasör ayarlarını hatırlama
- 🛡️ **Crash Protection**: Program çökmeyecek!
- 🎯 **Otomatik Emulator Bulma**: Popüler emulator'ları otomatik bulma

## 🚀 Kurulum

### 1. Python Kurulumu
Python 3.7+ gerekli. [python.org](https://python.org) adresinden indirebilirsin.

### 2. Gerekli Kütüphaneleri Yükle
```bash
pip install -r requirements.txt
```

### 3. Programı Çalıştır
```bash
python sega32x_player.py
```

## 🎮 Kullanım

### 1. Emulator Seçimi
- "📁 Emulator Seç" butonuna tıkla
- Sega 32X destekleyen emulator'ı seç (RetroArch, Mednafen, Kega Fusion, vb.)

### 2. Oyun Seçimi
**Tek Oyun:**
- "🎯 Tek Oyun Seç" ile tek dosya seç

**Çoklu Oyun:**
- "📂 Klasör Seç (Çoklu)" ile oyun klasörünü seç
- Program otomatik olarak tüm .32x, .rom, .bin, .smd dosyalarını bulur

### 3. Oyun Oynatma
- Listeden oyunu seç
- "▶️ OYNA!" butonuna tıkla
- Çift tıklama ile de oyun başlatabilirsin

### 4. Oyun Kontrolü
- "⏹️ DURDUR" ile oyunu durdur
- "🔄 Yenile" ile listeyi yenile

## 🎯 Desteklenen Emulator'lar

- **RetroArch** (retroarch.exe)
- **Mednafen** (mednafen.exe)
- **Kega Fusion** (fusion.exe)
- **Kega** (kega.exe)
- Diğer Sega 32X destekleyen emulator'lar

## 📁 Desteklenen Dosya Formatları

- `.32x` - Sega 32X ROM dosyaları
- `.rom` - ROM dosyaları
- `.bin` - Binary dosyalar
- `.smd` - Sega Mega Drive dosyaları

## 🛠️ Teknik Detaylar

- **GUI Framework**: Tkinter
- **Threading**: Oyun başlatma için ayrı thread'ler
- **Crash Protection**: Try-catch blokları ile hata yönetimi
- **Platform Support**: Windows, Linux, macOS
- **Settings**: JSON formatında ayar kaydetme

## 🔧 Sorun Giderme

### Program Çalışmıyor
- Python 3.7+ kurulu olduğundan emin ol
- Gerekli kütüphaneleri yükle: `pip install -r requirements.txt`

### Emulator Bulunamadı
- Emulator'ı manuel olarak seç
- Emulator'ın Sega 32X desteği olduğundan emin ol

### Oyun Başlamıyor
- ROM dosyasının bozuk olmadığından emin ol
- Emulator'ın doğru seçildiğini kontrol et

## 🎨 Ekran Görüntüleri

Program modern, koyu tema ile tasarlanmış ve kullanıcı dostu bir arayüze sahip!

## 📝 Lisans

Bu program açık kaynak kodludur ve eğitim amaçlı yapılmıştır.

## 🤝 Katkıda Bulunma

- Bug report'ları için issue aç
- Yeni özellik önerileri için pull request gönder

---

**🎮 Mutlu Oyunlar! 🎮**

*Program çökmeyecek, havada uçacak! 🚀*



