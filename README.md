# Advanced XSS Scanner

OWASP ZAP benzeri kapsamlı bir Cross-Site Scripting (XSS) güvenlik açığı tarayıcısı. Python ile yazılmış olup, requests ve BeautifulSoup kütüphanelerini kullanır.

## Özellikler

- 🔍 **Otomatik Form Tespiti**: Web sayfalarındaki tüm formları otomatik olarak tespit eder
- 💉 **Kapsamlı XSS Payload Veritabanı**: 300+ farklı XSS payload'u ile test yapar
- 🎯 **Çoklu XSS Türü Desteği**: 
  - Reflected XSS
  - DOM-based XSS
  - Stored XSS
- 🚀 **Gelişmiş Evasion Teknikleri**: WAF bypass teknikleri içerir
- 🧵 **Multi-threading Desteği**: Hızlı tarama için çoklu thread kullanır
- 📊 **Detaylı Raporlama**: Konsol ve dosya çıktısı ile kapsamlı raporlar
- 🔒 **Güvenlik Önerileri**: Bulunan açıklar için çözüm önerileri
- 🎨 **Renkli Terminal Çıktısı**: Kolay takip için renklendirilmiş sonuçlar

## Kurulum

### Gereksinimler

- Python 3.7+
- pip

### Bağımlılıkları Yükleme

```bash
pip install -r requirements.txt
```

### Manuel Kurulum

```bash
pip install requests beautifulsoup4 urllib3 lxml
```

## Kullanım

### Temel Kullanım

```bash
python xss_scanner.py -u http://example.com/login
```

### Gelişmiş Kullanım

```bash
# Çoklu thread ile hızlı tarama
python xss_scanner.py -u http://example.com -t 20 -d 0.5

# Özel User-Agent ile tarama
python xss_scanner.py -u http://example.com --user-agent "Custom Agent"

# Detaylı loglama ile tarama
python xss_scanner.py -u http://example.com -v

# Özel çıktı dosyası ile tarama
python xss_scanner.py -u http://example.com -o my_report.txt
```

### Parametreler

- `-u, --url`: Taranacak hedef URL (zorunlu)
- `-t, --threads`: Thread sayısı (varsayılan: 10)
- `-d, --delay`: İstekler arası gecikme (saniye, varsayılan: 1.0)
- `--timeout`: İstek timeout süresi (saniye, varsayılan: 30)
- `--user-agent`: Özel User-Agent string'i
- `-o, --output`: Detaylı rapor için çıktı dosyası (varsayılan: output.txt)
- `-v, --verbose`: Detaylı loglama

## Payload Kategorileri

### Temel Payloadlar
- Script tabanlı alert(), confirm(), prompt()
- Event handler tabanlı (onerror, onload, vb.)
- HTML injection teknikleri

### Gelişmiş Payloadlar
- JavaScript URL'leri (javascript:)
- Data URL'leri
- Eval ve Function constructor'ları
- DOM manipulation teknikleri

### Evasion Payloadlar
- Büyük/küçük harf varyasyonları
- Encoding teknikleri (URL, HTML entity, Unicode)
- Whitespace bypass teknikleri
- Comment injection

### WAF Bypass Payloadlar
- Filter bypass teknikleri
- Alternative quote kullanımı
- Template literal kullanımı
- Protocol bypass teknikleri

### Context-Specific Payloadlar
- Input field'lar için özel payloadlar
- Textarea escape teknikleri
- Select field bypass'ları
- URL context payloadları

## Çıktı Formatı

### Konsol Çıktısı
- Renkli ve organize edilmiş sonuçlar
- Real-time vulnerability bildirimleri
- Scan istatistikleri

### Dosya Çıktısı (output.txt)
- Detaylı vulnerability raporları
- Context analizi
- HTTP response bilgileri
- Güvenlik önerileri

## Güvenlik Özellikleri

### False Positive Azaltma
- Escaped content tespiti
- Safe context analizi
- Multiple pattern matching

### Risk Değerlendirmesi
- Critical, High, Medium, Low risk seviyeleri
- Confidence skorları
- Context-based risk assessment

### Advanced Detection
- DOM-based XSS indicators
- Attribute injection detection
- JavaScript context analysis

## Örnek Çıktı

```
Advanced XSS Scanner v1.0
==================================================
Target URL: http://example.com/login
Threads: 10
Delay: 1.0s
Timeout: 30s

[1/4] Discovering forms...
[INFO] Fetching target URL: http://example.com/login
[SUCCESS] Found 2 form(s)

[2/4] Analyzing forms...
[INFO] Analyzing form structures...

[3/4] Generating payloads...
[INFO] Generating XSS payloads...
[SUCCESS] Generated 342 payloads

[4/4] Testing for XSS vulnerabilities...
[INFO] Testing XSS vulnerabilities with 10 threads...
[VULN] XSS found in form login_form, parameter username

[CRITICAL] XSS VULNERABILITIES FOUND!
============================================================

Vulnerability #1:
URL: http://example.com/process_login
Form ID: login_form
Parameter: username
Method: POST
Payload: <script>alert('XSS')</script>
Detection: XSS detected: <script>alert('XSS')</script>
Risk Level: Critical
Confidence: High
```

## Güvenlik Uyarıları

⚠️ **Yasal Uyarı**: Bu araç yalnızca size ait olan veya test etme izniniz olan web sitelerinde kullanılmalıdır.

⚠️ **Etik Hacking**: Bu araç penetration testing ve güvenlik araştırmaları için tasarlanmıştır.

⚠️ **Sorumluluk**: Bu aracın kötüye kullanımından doğacak zararlardan geliştiriciler sorumlu değildir.

## Katkıda Bulunma

1. Bu repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## İletişim

Sorularınız için issue açabilir veya pull request gönderebilirsiniz.

## Changelog

### v1.0.0
- İlk sürüm
- Temel XSS tarama özellikleri
- Multi-threading desteği
- Kapsamlı payload veritabanı
- Detaylı raporlama sistemi 



