# XenForo Forum Website

Modern, responsive forum website built with HTML, CSS, and JavaScript that mimics the design and functionality of XenForo.

## 🌟 Özellikler

### 🎨 Tasarım
- **Modern ve Responsive Tasarım**: Tüm cihazlarda mükemmel görünüm
- **Gradient Renkler**: XenForo tarzı gradient header ve butonlar
- **Smooth Animasyonlar**: Sayfa yüklenirken ve etkileşimlerde yumuşak geçişler
- **Font Awesome İkonları**: Profesyonel görünüm için modern ikonlar

### 📱 Responsive Özellikler
- **Mobile-First Yaklaşım**: Mobil cihazlarda optimize edilmiş görünüm
- **Hamburger Menü**: Mobil cihazlarda gizlenebilir navigasyon
- **Esnek Grid Sistemi**: Farklı ekran boyutlarında uyumlu layout

### ⚡ İnteraktif Özellikler
- **Arama Fonksiyonu**: Forum içeriğinde arama yapabilme
- **Smooth Scrolling**: Sayfa içi linklerde yumuşak kaydırma
- **Bildirim Sistemi**: Kullanıcı etkileşimleri için bildirimler
- **Loading Animasyonları**: Sayfa geçişlerinde yükleme göstergeleri
- **Hover Efektleri**: Forum öğelerinde etkileşimli hover efektleri

### 🎯 Forum Özellikleri
- **Kategori Sistemi**: Ana ve teknik kategoriler
- **Forum Listesi**: Her kategori için ayrı forum alanları
- **Son Konular**: En güncel forum konuları
- **Üye Profilleri**: Aktif üyelerin profilleri
- **İstatistikler**: Üye, konu ve mesaj sayıları

## 📁 Dosya Yapısı

```
xenforo-forum/
├── index.html          # Ana HTML dosyası
├── styles.css          # CSS stilleri
├── script.js           # JavaScript fonksiyonları
└── README.md           # Proje dokümantasyonu
```

## 🚀 Kurulum

1. **Dosyaları İndirin**: Tüm dosyaları bilgisayarınıza indirin
2. **Web Sunucusu**: Dosyaları bir web sunucusuna yükleyin veya localhost'ta çalıştırın
3. **Tarayıcıda Açın**: `index.html` dosyasını tarayıcınızda açın

### Localhost'ta Çalıştırma

```bash
# Python ile basit HTTP sunucusu
python -m http.server 8000

# Node.js ile (http-server paketi gerekli)
npx http-server

# PHP ile
php -S localhost:8000
```

## 🎨 Özelleştirme

### Renkleri Değiştirme
`styles.css` dosyasında aşağıdaki CSS değişkenlerini düzenleyebilirsiniz:

```css
/* Ana renkler */
--primary-color: #667eea;
--secondary-color: #764ba2;
--accent-color: #ffd700;
```

### İçerik Ekleme
`index.html` dosyasında forum kategorileri ve konuları ekleyebilirsiniz:

```html
<div class="forum-item">
    <div class="forum-icon">
        <i class="fas fa-icon-name"></i>
    </div>
    <div class="forum-info">
        <h4><a href="#">Forum Adı</a></h4>
        <p>Forum açıklaması</p>
    </div>
</div>
```

## 📱 Mobil Uyumluluk

Website aşağıdaki cihazlarda test edilmiştir:
- ✅ iPhone (iOS Safari)
- ✅ Android (Chrome)
- ✅ iPad (Safari)
- ✅ Desktop (Chrome, Firefox, Safari, Edge)

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler
- **HTML5**: Semantic markup
- **CSS3**: Modern styling ve animations
- **JavaScript (ES6+)**: İnteraktif özellikler
- **Font Awesome**: İkonlar
- **Google Fonts**: Typography

### Browser Desteği
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 🎯 Gelecek Özellikler

- [ ] Kullanıcı kayıt/giriş sistemi
- [ ] Forum konuları için detay sayfaları
- [ ] Yorum sistemi
- [ ] Dosya yükleme özelliği
- [ ] Admin paneli
- [ ] Dark mode
- [ ] Çoklu dil desteği

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 📞 İletişim

- **Email**: info@xenforo.com
- **Telefon**: +90 555 123 4567
- **Website**: https://xenforo.com

## 🙏 Teşekkürler

- Font Awesome ikonları için
- Google Fonts tipografi için
- Modern web standartları için

---

**Not**: Bu proje eğitim amaçlı oluşturulmuştur ve gerçek XenForo yazılımı ile ilişkisi yoktur.



