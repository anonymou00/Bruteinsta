# Toplu SMS Gönderici

Bu uygulama, toplu SMS gönderimi için geliştirilmiş bir GUI uygulamasıdır.

## Özellikler

- Modern ve kullanıcı dostu GUI arayüzü
- TXT dosyasından numara listesi okuma
- Özelleştirilebilir mesaj
- Ayarlanabilir gönderim hızı
- Gerçek zamanlı ilerleme takibi
- Detaylı log kayıtları
- İstatistik raporları

## Kurulum

1. Python 3.7+ yüklü olmalıdır
2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

1. Uygulamayı başlatın:
```bash
python sms_sender.py
```

2. "Dosya Seç" butonuna tıklayarak numara listesi dosyasını seçin
3. Mesaj metnini yazın
4. Gönderim hızını ayarlayın (ms cinsinden)
5. "Gönderimi Başlat" butonuna tıklayın

## Numara Dosyası Formatı

Numara dosyası (.txt) şu formatta olmalıdır:
```
+905551234567
+905551234568
+905551234569
```

Her satırda bir numara olmalıdır.

## SMS API Entegrasyonu

Gerçek SMS gönderimi için `send_sms` fonksiyonunu SMS sağlayıcınızın API'sine göre güncelleyin:

```python
def send_sms(self, phone_number, message):
    try:
        payload = {
            'phone': phone_number,
            'message': message,
            'api_key': self.api_key
        }
        response = requests.post(self.api_url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        return False
```

## Güvenlik Notları

- Bu uygulamayı sadece yasal amaçlar için kullanın
- SMS gönderimi için gerekli izinleri alın
- API anahtarlarını güvenli şekilde saklayın
- Spam filtrelerini tetiklememek için uygun hız ayarları yapın

## Lisans

Bu proje eğitim amaçlıdır. Ticari kullanım için gerekli lisansları alın. 



