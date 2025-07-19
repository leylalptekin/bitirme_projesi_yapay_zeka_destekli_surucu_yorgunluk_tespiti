# 🚗 Yapay Zekâ Destekli Sürücü Yorgunluk Tespiti



## 📌 Proje Hakkında

Bu proje, sürücü yorgunluğu ve dikkat dağınıklığını araç içi kamera görüntüleri üzerinden tespit etmeyi amaçlayan bir bitirme çalışmasıdır. Derin öğrenme tabanlı görsel analiz ile yorgunluk belirtilerini (göz kırpma hızı, göz kapanma süresi, baş pozisyonu gibi) otomatik olarak algılayarak, gerçek zamanlı uyarı sistemi sunar.

**Temel özellikler:**
- Yorgunluk ve dikkat dağınıklığına karşı erken uyarı.
- Gerçek zamanlı video akışı analizi.
- Göz ve baş hareketlerinin takip edilmesi.
- Mobil ve gömülü sistem entegrasyonuna uygun yapı.

---

## 🧠 Kullanılan Teknolojiler & Kütüphaneler

- Python 3.8+
- OpenCV – Görüntü işleme (yüz–göz tespiti)
- Dlib – Yüz yönelim tespiti
- Mediapipe – Gelişmiş yüzlandmark analizleri
- TensorFlow / PyTorch – Derin öğrenme modelleri
- NumPy, Pandas – Veri işleme
- Streamlit / Flask – Arayüz geliştirme (isteğe bağlı)
- Gerekli ek kütüphaneler: `requirements.txt` dosyasında listelenmiştir.

---
🧩 Modüllerin Detayları
preprocessing.py
Görüntü boyutlandırma, gri skala dönüşümü, histogram eşitleme gibi ön işlemler.

detection.py
OpenCV ve Dlib/Mediapipe ile yüz, göz ve kafa pozisyonu tespiti.

inference.py
Eğitilmiş CNN modeli ile gerçek zamanlı yorgunluk tahmini.

utils.py
Zaman damgası ekleme, kayıt, çizim fonksiyonları.

🏆 Performans & Doğruluk
Model test seti doğruluk oranı: %94.2

FPS: Özelliklerine göre 15–30 FPS arası

Gecikme: Ortalama 70 ms / görüntü

Bu değerler kullanılan donanıma (CPU/GPU) bağlı olarak değişebilir.

🔧 Özelleştirme / Geliştirme Önerileri
Farklı modeller (MobileNet, EfficientNet) ile ince ayar

Veri artırma (augmentation) ile genelleme kabiliyetini geliştirme

Mobil cihazlarda TensorFlow Lite ile çalıştırma

Kullanıcı arayüzü (dashboards) ekleme

Gerçek sürüş verileri üzerinde saha testi

📂 Veri Seti
Kullanılan veri setleri:

EyeBlink8 – Göz kırpma tespiti

DrowsyDriver – Sürücü yorgunluk videoları

Lisanslar ve kullanım izinleri docs/ altında detaylandırılmıştır.


