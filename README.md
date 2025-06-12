# YOLO ve OpenCV ile Gerçek Zamanlı Güvenlik Kamerası Uygulaması

[cite_start]Bu proje, **Mustafa Buğra OKURER** tarafından Gazi Üniversitesi Teknoloji Fakültesi Elektrik Elektronik Mühendisliği Bölümü'nde lisans tezi olarak geliştirilmiştir. 

[cite_start]Proje, bir güvenlik kamerasından alınan gerçek zamanlı video akışını `YOLOv8` nesne tespiti ve `face_recognition` yüz tanıma kütüphanelerini kullanarak işler.  [cite_start]Belirlenen bir alana izinsiz girişleri tespit ederek alarm çalar ve e-posta yoluyla uyarı gönderir. 

---

## 🌟 Projenin Amacı

[cite_start]Bu çalışmanın temel amacı, YOLO nesne tanıma algoritması ve OpenCV görüntü işleme kütüphanesini kullanarak gerçek zamanlı bir güvenlik kamerası uygulaması geliştirmektir.  [cite_start]Geliştirilen sistem, mevcut güvenlik sistemlerinin yetersizliklerini gidermeyi, izinsiz girişleri yüksek doğruluk ve hızla tespit ederek  [cite_start]alarm tetikleme ve e-posta ile bildirim gönderme gibi güvenlik fonksiyonları sunmayı hedeflemektedir. 

## 🚀 Özellikler

* **Gerçek Zamanlı Video Akışı**: Kameradan alınan görüntülerin anlık olarak kullanıcı arayüzünde gösterilmesi.
* [cite_start]**İzinsiz Alan Belirleme**: Kullanıcının fare ile ekranda bir "yasak bölge" çizerek izlenmesini istediği alanı dinamik olarak belirleyebilmesi. 
* [cite_start]**Yüksek Başarımlı Nesne Tespiti**: `YOLOv8` modeli kullanılarak insan tespiti yapılması. 
* [cite_start]**Yüz Tanıma**: Sisteme önceden tanıtılan kişileri tanıma ve tanınmayanları "yetkisiz" olarak işaretleme. 
* [cite_start]**Akıllı Alarm Sistemi**: Tanınmayan bir kişi belirlenen alana girdiğinde `Pygame` ile sesli alarm çalınması. 
* [cite_start]**Anlık E-posta Bildirimi**: Alarm durumunda, `smtplib` kütüphanesi ile olay anının fotoğrafını çekip belirtilen e-posta adresine uyarı olarak gönderme. 
* [cite_start]**Kullanıcı Dostu Arayüz**: `Tkinter` ile oluşturulmuş, kullanımı kolay bir arayüz. 
* [cite_start]**Detaylı Olay Kaydı (Log)**: Tespit edilen her olayın zaman damgasıyla birlikte arayüzdeki log ekranına yazdırılması. 

## 🛠️ Kurulum ve Kullanım

### Gereksinimler

* Python 3.8+
* [cite_start]Yüksek çözünürlüklü bir kamera. 
* `CMake` ve `dlib` kütüphanesinin kurulabilmesi için gerekli C++ derleyicisi.

### Kurulum Adımları

1.  **Projeyi Klonlayın:**
    ```bash
    git clone [SENİN_GITHUB_REPO_LİNKİN]
    cd [PROJE_KLASOR_ADIN]
    ```

2.  **Gerekli Dosyaları Hazırlayın:**
    * YOLOv8 modelini (`yolov8n.pt`) [buradan](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt) indirin ve projenin ana dizinine kaydedin.
    * Bir alarm sesini `Tehlike Alarm Sesi.mp3` olarak ana dizine ekleyin.
    * Tanınmasını istediğiniz kişilerin fotoğraflarını (`isim.jpg` formatında) `known_faces` adında bir klasör oluşturup içine ekleyin.

3.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

### Yapılandırma

`guvenlik.py` dosyasında e-posta gönderecek ve alacak adresleri kendi bilgilerinizle güncelleyin.
```python
EMAIL_ADDRESS = 'ornek@gmail.com'
EMAIL_PASSWORD = 'UYGULAMA_SIFRENIZ' # Normal şifreniz değil, Google 'Uygulama Şifresi' kullanın.
TO_EMAIL = 'uyari_gonderilecek_adres@gmail.com'
```

### Çalıştırma

```bash
python guvenlik.py
```

## 💻 Kullanılan Kütüphane ve Teknolojiler

Bu projede kullanılan kütüphane ve teknolojiler şunlardır:

* [cite_start]**OpenCV:** Güvenlik kamerasından görüntülerin işlenmesi ve analizi için kullanılmıştır. 
* [cite_start]**YOLO (Ultralytics):** Gerçek zamanlı nesne algılama için `YOLOv8` modeli kullanılmıştır. 
* [cite_start]**Face_recognition:** Yüz tanıma ve karşılaştırma işlemleri için kullanılmıştır. 
* **Pygame:** Yetkisiz giriş durumunda alarm sesi çalmak için kullanılmıştır. 
* [cite_start]**smtplib ve email:** Tespit edilen yetkisiz giriş sonrası e-posta ile uyarı göndermek için kullanılmıştır. 
* [cite_start]**Tkinter:** Kullanıcıların sistemi yönetebilmesi için grafiksel kullanıcı arayüzü (GUI) oluşturmak amacıyla kullanılmıştır. 
* **NumPy:** Yüz tanıma ve nesne tespiti algoritmalarında sayısal verilerin verimli bir şekilde işlenmesi için kullanılmıştır. 
* [cite_start]**PIL (Pillow):** Görüntülerin işlenip Tkinter arayüzünde gösterilmesi için kullanılmıştır. 
* [cite_start]**Threading:** Görüntü işleme ve kullanıcı arayüzü işlemlerinin aynı anda kesintisiz çalışabilmesi için kullanılmıştır. 

## 🙏 Teşekkür

Çalışmalarım boyunca değerli yardım ve katkılarıyla beni yönlendiren saygıdeğer hocam **Prof. [cite_start]Dr. İbrahim SEFA**'ya teşekkürü bir borç bilirim.