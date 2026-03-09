# 🎤 Echo-Translate AI Pro: Gelişmiş Sesli Tercüman

**Echo-Translate**, yapay zeka destekli anlık sesli çeviri asistanıdır. Konuşmanızı dinler, istediğiniz dile tercüme eder, Microsoft Edge TTS teknolojisiyle seslendirir ve çıktıları bir bütün olarak (MP3 + PDF) indirmenize imkan tanır.

---

## 📂 Proje Dosya Yapısı

```text
echo_translate/
├── app.py                  # Ana Streamlit uygulama kodumuz
├── requirements.txt        # Gerekli Python kütüphanelerinin listesi
├── README.md               # Proje açıklaması ve kullanım kılavuzu
└── .gitignore              # GitHub'a gönderilmeyecek dosyalar (örn: output.mp3)
```

---

## ✨ Özellikler

-   🌍 **Çok Dilli Destek:** 11 Farklı dil arasında (Türkçe, İngilizce, Arapça, Rusça, Çince, Japonca vb.) çift yönlü anlık çeviri.
-   🗣️ **Gelişmiş Ses Sentezi (TTS):** Microsoft Edge TTS altyapısı ile 10 farklı (5 Kadın, 5 Erkek) doğal ses tonu seçeneği.
-   🎙️ **Ses Tanıma:** Google Speech Recognition ile yüksek doğrulukta ses-metin dönüşümü.
-   📥 **Akıllı İndirme Paketi:** Çeviri sonrasında hem **MP3** ses kaydını hem de **PDF** transkriptini içeren tek bir ZIP dosyası oluşturma.
-   📄 **PDF Transkript:** Kaynak ve hedef metinleri içeren, Unicode (Arapça, Rusça vb.) destekli raporlama.

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/nejdettut/Echo-Translate-104.git
cd Echo-Translate-104
```

### 2. Bağımlılıkları Yükleyin
```bash
python -m pip install -r echo_translate/requirements.txt
```
*Not: Windows kullanıcıları için mikrofon desteği adına `pip install pyaudio` gerekebilir.*

### 3. Uygulamayı Başlatın
```bash
streamlit run echo_translate/app.py
```

---

## 🖥️ Teknolojiler

-   **Frontend:** Streamlit
-   **Tercüme:** Googletrans (4.0.0-rc1)
-   **Ses Tanıma:** SpeechRecognition
-   **Ses Sentezi:** Microsoft Edge TTS
-   **Raporlama:** FPDF2
-   **Programlama Dili:** Python 3.12+

---

## ✍️ Tasarım ve Geliştirme

Bu proje bütünüyle bir entegrasyon çalışmasıdır.

**Designed by © 2026 Nejdet Tut**
