# YOLO ve OpenCV ile Gerçek Zamanlı Güvenlik Kamerası Uygulaması

*Real-Time Security Camera Application with YOLO and OpenCV*

Bu proje, **Mustafa Buğra OKURER** tarafından Gazi Üniversitesi Teknoloji Fakültesi Elektrik Elektronik Mühendisliği Bölümü'nde lisans tezi olarak geliştirilmiştir.

This project was developed by **Mustafa Buğra OKURER** as an undergraduate thesis at Gazi University Faculty of Technology, Department of Electrical and Electronics Engineering.

Proje, bir güvenlik kamerasından alınan gerçek zamanlı video akışını `YOLOv8` nesne tespiti ve `face_recognition` yüz tanıma kütüphanelerini kullanarak işler. Belirlenen bir alana izinsiz girişleri tespit ederek alarm çalar ve e-posta yoluyla uyarı gönderir.

The application processes real-time video from a security camera using `YOLOv8` for object detection and the `face_recognition` library. It detects unauthorized entry into a predefined area, triggers an alarm, and sends an email notification.

---

## 🌟 Projenin Amacı

Bu çalışmanın temel amacı, YOLO nesne tanıma algoritması ve OpenCV görüntü işleme kütüphanesini kullanarak gerçek zamanlı bir güvenlik kamerası uygulaması geliştirmektir. Geliştirilen sistem, mevcut güvenlik sistemlerinin yetersizliklerini gidermeyi, izinsiz girişleri yüksek doğruluk ve hızla tespit ederek alarm tetikleme ve e-posta ile bildirim gönderme gibi güvenlik fonksiyonları sunmayı hedeflemektedir.

*Purpose:* Develop a real-time security camera system using the YOLO object detection algorithm and OpenCV. The system aims to overcome limitations of existing solutions by accurately detecting intrusions, triggering alarms, and sending email alerts.

## 🚀 Özellikler

- **Gerçek Zamanlı Video Akışı**: Kameradan alınan görüntülerin anlık olarak kullanıcı arayüzünde gösterilmesi.
- **İzinsiz Alan Belirleme**: Kullanıcının fare ile ekranda bir "yasak bölge" çizerek izlenmesini istediği alanı dinamik olarak belirleyebilmesi.
- **Yüksek Başarımlı Nesne Tespiti**: `YOLOv8` modeli kullanılarak insan tespiti yapılması.
- **Yüz Tanıma**: Sisteme önceden tanıtılan kişileri tanıma ve tanınmayanları "yetkisiz" olarak işaretleme.
- **Akıllı Alarm Sistemi**: Tanınmayan bir kişi belirlenen alana girdiğinde `Pygame` ile sesli alarm çalınması.
- **Anlık E-posta Bildirimi**: Alarm durumunda, `smtplib` kütüphanesi ile olay anının fotoğrafını çekip belirtilen e-posta adresine uyarı olarak gönderme.
- **Kullanıcı Dostu Arayüz**: `Tkinter` ile oluşturulmuş, kullanımı kolay bir arayüz.
- **Detaylı Olay Kaydı (Log)**: Tespit edilen her olayın zaman damgasıyla birlikte arayüzdeki log ekranına yazdırılması.

*Features (English):*
- **Real-Time Video Feed** displayed in the interface.
- **Restricted Area Selection** drawn with the mouse.
- **High-Performance Detection** of people using `YOLOv8`.
- **Face Recognition** to mark unknown persons as unauthorized.
- **Smart Alarm** with sound via `Pygame`.
- **Instant Email Alerts** with a captured image.
- **User-Friendly Interface** built with `Tkinter`.
- **Detailed Logging** of all detected events.

## 🛠️ Kurulum ve Kullanım

### Gereksinimler / Requirements

- Python 3.8+
- Yüksek çözünürlüklü bir kamera / A high-resolution camera
- `CMake` ve `dlib` kütüphanesinin kurulabilmesi için gerekli C++ derleyicisi / A C++ compiler for `CMake` and `dlib`

### Kurulum Adımları / Installation

1. **Projeyi Klonlayın / Clone the repository**
   ```bash
   git clone [SENİN_GITHUB_REPO_LİNKİN]
   cd [PROJE_KLASOR_ADIN]
   ```
2. **Gerekli Dosyaları Hazırlayın / Prepare required files**
   - YOLOv8 modelini (`yolov8n.pt`) [buradan](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt) indirin ve projenin ana dizinine kaydedin.
   - Bir alarm sesini `Tehlike Alarm Sesi.mp3` olarak ana dizine ekleyin.
   - Tanınmasını istediğiniz kişilerin fotoğraflarını (`isim.jpg` formatında) `known_faces` klasörüne yerleştirin.
3. **Gerekli Kütüphaneleri Yükleyin / Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```


### Yapılandırma / Configuration

2.  **Gerekli Dosyaları Hazırlayın:**
    * YOLOv8 modelini (`yolov8n.pt`) [buradan](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt) indirin ve projenin ana dizinine kaydedin.
    * Bir alarm sesini `Tehlike Alarm Sesi.mp3` olarak ana dizine ekleyin.
    * Tanınmasını istediğiniz kişilerin fotoğraflarını (`isim.jpg` formatında) `known_faces` adında bir klasör oluşturup içine ekleyin.

3.  **Gerekli Kütüphaneleri Yükleyin:** Projenin kök dizinindeki
   `requirements.txt` dosyasında listelenen bağımlılıkları yüklemek için:
    ```bash
    pip install -r requirements.txt
    ```




`guvenlik.py` dosyasında e-posta gönderecek ve alacak adresleri kendi bilgilerinizle güncelleyin.
Update the email credentials in `guvenlik.py`.
```python
EMAIL_ADDRESS = 'ornek@gmail.com'
EMAIL_PASSWORD = 'UYGULAMA_SIFRENIZ'  # Google "Uygulama Şifresi" kullanın
TO_EMAIL = 'uyari_gonderilecek_adres@gmail.com'
```


### Çalıştırma / Running

### Kamerayı Kendi Kaynağınıza Bağlama

`guvenlik.py` dosyasında kamera görüntüsü `cv2.VideoCapture()` fonksiyonu
kullanılarak açılır. Varsayılan olarak yerel bilgisayarınızdaki kamera
`cv2.VideoCapture(0)` ile seçilmiştir. Kendi IP kameranızın adresini ya da
farklı bir kamera ID'si kullanmak için bu satırı şu şekilde güncelleyebilirsiniz:

```python
cap = cv2.VideoCapture("<KAMERA_URL_VEYA_ID>")
```

Örneğin bir IP kamera için `cv2.VideoCapture("rtsp://<adres>")` ya da ikinci
USB kamera için `cv2.VideoCapture(1)` yazabilirsiniz.

### Çalıştırma


```bash
python guvenlik.py
```

## 💻 Kullanılan Kütüphane ve Teknolojiler

Bu projede kullanılan kütüphane ve teknolojiler şunlardır / The project uses:

- **OpenCV** – görüntülerin işlenmesi için / image processing
- **YOLO (Ultralytics)** – gerçek zamanlı nesne algılama / real-time object detection
- **Face_recognition** – yüz tanıma ve karşılaştırma / facial recognition
- **Pygame** – alarm sesi çalmak için / playing the alarm sound
- **smtplib ve email** – e-posta uyarısı göndermek için / sending email alerts
- **Tkinter** – grafiksel kullanıcı arayüzü / GUI
- **NumPy** – sayısal verileri işlemek için / numeric processing
- **PIL (Pillow)** – görüntüleri işlemek ve arayüzde göstermek için / image display
- **Threading** – aynı anda kesintisiz çalışmak için / concurrent execution

## 🙏 Teşekkür / Acknowledgment

Çalışmalarım boyunca değerli yardım ve katkılarıyla beni yönlendiren saygıdeğer hocam **Prof. Dr. İbrahim SEFA**'ya teşekkürü bir borç bilirim.

I would like to thank my esteemed advisor **Prof. Dr. İbrahim SEFA** for his invaluable guidance and support.
