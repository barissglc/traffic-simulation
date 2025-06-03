# Ajan Tabanlı Trafik Kavşağı Simülasyonu

Bu proje, farklı trafik kontrol stratejilerinin performansını analiz etmek ve karşılaştırmak amacıyla geliştirilmiş ajan tabanlı bir trafik kavşağı simülasyonudur. Simülasyon, Python programlama dili ve Pygame kütüphanesi kullanılarak oluşturulmuştur.

## Projenin Amacı

Kent yaşamında önemli bir sorun olan trafik sıkışıklığına çözüm aramak amacıyla, farklı trafik kontrol stratejilerinin (eşit öncelik, ana yol önceliği, gelişmiş ana yol önceliği ve adaptif zamanlama) etkinliklerini bilgisayar simülasyonu ile karşılaştırmak ve en optimal çözümü belirlemektir.

## Kurulum ve Çalıştırma

1.  **Gereksinimler:**
    *   Python 3.x
    *   Pygame kütüphanesi

2.  **Kurulum:**
    Proje dosyalarını bilgisayarınıza indirin. Gerekli kütüphaneleri yüklemek için aşağıdaki komutu terminalde çalıştırın:
    ```bash
    pip install pygame
    ```

3.  **Çalıştırma:**
    Simülasyonu başlatmak için `main.py` dosyasını çalıştırın:
    ```bash
    python main.py
    ```
    Simülasyon başladığında, farklı trafik kontrol stratejilerini deneyebilir ve sonuçlarını gözlemleyebilirsiniz. `config.py` dosyası üzerinden simülasyon parametrelerini (simülasyon süresi, araç sayısı, hızlar vb.) değiştirebilirsiniz.

## Dosya Yapısı

```
traffic_simulation/
├── assets/                # Kullanılıyorsa resim, ses gibi varlıklar için
├── config.py              # Simülasyon ayar ve parametreleri
├── intersection.py        # Kavşak yönetimi ve trafik kontrol stratejileri
├── main.py                # Ana simülasyon döngüsü ve uygulama girişi
├── vehicle.py             # Araç ajanlarının tanımı ve davranışları
├── visualization.py       # Simülasyonun görselleştirilmesi (Pygame ile)
└── README.md              # Bu dosya
```

## İncelenen Trafik Kontrol Stratejileri

Simülasyonda aşağıdaki dört farklı trafik kontrol stratejisi modellenmiş ve karşılaştırılmıştır:

1.  **Eşit Öncelik (Equal Priority):** Tüm yönlerden gelen araçlara eşit geçiş hakkı tanır.
2.  **Ana Yol Önceliği (Main Road Priority):** Belirlenen ana yoldaki araçlara mutlak öncelik verir.
3.  **Gelişmiş Ana Yol Önceliği (Enhanced Main Road Priority):** Ana yola öncelik verirken, belirli aralıklarla yan yollara da geçiş hakkı tanır.
4.  **Adaptif Zamanlama (Adaptive Timing):** Anlık trafik yoğunluğuna göre geçiş önceliklerini dinamik olarak ayarlar.

## Temel Bulgular (Simülasyon Raporundan)

Yapılan simülasyonlar sonucunda elde edilen temel bulgular şunlardır:

*   **Adaptif Zamanlama Stratejisi:** En yüksek araç geçiş kapasitesini (379 araç) ve çok düşük ortalama bekleme süresini (0.18s) sunarak en verimli strateji olarak öne çıkmıştır.
*   **Ana Yol Önceliği Stratejisi:** En düşük ortalama bekleme süresini (0.17s) sağlamasına rağmen, yan yolları tamamen ihmal etmesi nedeniyle pratik uygulamalar için uygun değildir.
*   **Gelişmiş Ana Yol Önceliği Stratejisi:** 249 araç kapasitesi ve 0.42s bekleme süresi ile dengeli bir performans sergilemiştir.
*   **Eşit Öncelik Stratejisi:** 195 araç kapasitesi ile en düşük performansı göstermiştir.

Bu bulgular, kent içi trafik yönetiminde adaptif ve akıllı sistemlerin potansiyel faydalarını göstermektedir.
