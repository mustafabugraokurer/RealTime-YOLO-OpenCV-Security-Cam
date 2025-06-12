import cv2
from ultralytics import YOLO
import smtplib
from email.message import EmailMessage
import os
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime
import pygame
import pickle  # Yüz verilerini kaydetmek ve yüklemek için

# Modeli yükleniyor
model = YOLO('yolov8n.pt')  # YOLOv8 model yolunu burada belirtin

# Kamerayı açın
cap = cv2.VideoCapture("192.168.1.5:4747")

# Kamera açıkken işlem yapılıyor mu kontrol etmek için değişken tanımlayın
camera_open = True

# İzinsiz giriş alanı için başlangıç ve bitiş koordinatlarını tanımlayın
entry_zone_top_left = None
entry_zone_bottom_right = None
drawing = False

# Tanınan yüzlerin encode'larını saklayın
known_face_encodings = []
known_face_names = []
recognized_names = set()

# Tanınan yüz verilerini kaydedeceğimiz dosya
face_data_file = 'face_data.pkl'

# Yüz verilerini kaydetme fonksiyonu
def save_face_data():
    with open(face_data_file, 'wb') as f:
        face_data = {'encodings': known_face_encodings, 'names': known_face_names}
        pickle.dump(face_data, f)

# Yüz verilerini yükleme fonksiyonu
def load_face_data():
    global known_face_encodings, known_face_names
    if os.path.exists(face_data_file):
        with open(face_data_file, 'rb') as f:
            face_data = pickle.load(f)
            known_face_encodings = face_data['encodings']
            known_face_names = face_data['names']

# Program başlatıldığında yüz verilerini yükleyin
load_face_data()

# Alarm durumu ve e-posta gönderimini kontrol eden değişkenler
alarm_triggered = False
send_email_flag = True

# Pygame'i başlat ve alarm sesini yükle
pygame.mixer.init()
pygame.mixer.music.load('Tehlike Alarm Sesi.mp3')

# E-posta gönderim fonksiyonu
def send_email(image_path):
    global send_email_flag
    if not send_email_flag:
        print("E-posta gönderme şu anda devre dışı.")
        return

    EMAIL_ADDRESS = 'ornek@gmail.com'
    EMAIL_PASSWORD = 'UYGULAMA_SIFRENIZ' # Normal şifreniz değil, Google 'Uygulama Şifresi' kullanın.
    TO_EMAIL = 'uyari_gonderilecek_adres@gmail.com'

    msg = EmailMessage()
    msg['Subject'] = 'Güvenlik Uyarısı: Yetkisiz Giriş Algılandı'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg.set_content('Yetkisiz giriş tespit edildi. Ekteki resme bakınız.')

    try:
        print("Resim dosyasını açmaya çalışıyorum...")
        with open(image_path, 'rb') as img:
            img_data = img.read()
            msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename=os.path.basename(image_path))
        print("Resim dosyasi başarıyla açıldı.")

        print("SMTP sunucusuna bağlanmaya çalışılıyor...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("E-posta başarıyla gönderildi.")
    except smtplib.SMTPAuthenticationError:
        print("E-posta gönderilemedi: Kimlik doğrulama hatası. E-postanızı ve şifrenizi kontrol edin.")
    except smtplib.SMTPConnectError:
        print("E-posta gönderilemedi: SMTP sunucusuna bağlanılamadı.")
    except Exception as e:
        print(f"E-posta gönderilemedi: {e}")

# Alan hesaplama fonksiyonu
def calculate_area(x1, y1, x2, y2):
    return abs((x2 - x1) * (y2 - y1))

# Kesişim alanı hesaplama fonksiyonu
def calculate_intersection_area(box1, box2):
    x_left = max(box1[0], box2[0])
    y_top = max(box1[1], box2[1])
    x_right = min(box1[2], box2[2])
    y_bottom = min(box1[3], box2[3])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    return calculate_area(x_left, y_top, x_right, y_bottom)

# Fare olayları için callback fonksiyonu
def draw_rectangle(event, x, y, flags, param):
    global entry_zone_top_left, entry_zone_bottom_right, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        entry_zone_top_left = (x, y)
        entry_zone_bottom_right = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            entry_zone_bottom_right = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        entry_zone_bottom_right = (x, y)

# Yeni yüz kaydetme fonksiyonu
def add_new_face(name):
    ret, frame = cap.read()
    if not ret:
        print("Kameradan görüntü alınamıyor.")
        return

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    if len(face_locations) != 1:
        print("Lütfen sadece bir yüz içeren bir görüntü sağlayın.")
        return

    face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]

    known_face_encodings.append(face_encoding)
    known_face_names.append(name)

    # Yeni yüz kaydedildiğinde log yazısı ekleyin
    app.log_text.insert(tk.END, f"{datetime.now()}: Yeni yüz eklendi: {name}\n")

    # Yüz verilerini dosyaya kaydedin
    save_face_data()

    # Yüzü dosyaya kaydedin
    face_image_path = f"{name}.jpg"
    cv2.imwrite(face_image_path, frame)
    print(f"Yeni yüz kaydedildi ve {face_image_path} dosyasına kaydedildi.")

# Arayüz sınıfı
class SecurityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Güvenlik Kamerası")

        # Video gösterim alanı
        self.video_label = ttk.Label(root)
        self.video_label.pack()

        # Log gösterim alanı
        self.log_text = tk.Text(root, height=10, width=50)
        self.log_text.pack()

        # Alarm butonları
        self.alarm_button = ttk.Button(root, text="Alarm", command=self.trigger_alarm)
        self.alarm_button.pack()
        self.reset_button = ttk.Button(root, text="Alarm Sıfırlama", command=self.reset_alarm)
        self.reset_button.pack()

        # Yeni yüz ekleme butonu
        self.create_add_face_button()

        # Fare olaylarını ayarla
        self.video_label.bind("<ButtonPress-1>", self.on_mouse_down)
        self.video_label.bind("<B1-Motion>", self.on_mouse_move)
        self.video_label.bind("<ButtonRelease-1>", self.on_mouse_up)

        self.processing_thread = threading.Thread(target=self.process_frames)
        self.processing_thread.daemon = True
        self.processing_thread.start()

        # Timer ile video güncelleme
        self.update_video()

    def create_add_face_button(self):
        add_face_button = ttk.Button(self.root, text="Yeni Yüz Ekle", command=self.open_add_face_window)
        add_face_button.pack()

    def open_add_face_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Yeni Yüz Ekle")

        tk.Label(new_window, text="İsim:").pack()
        name_entry = tk.Entry(new_window)
        name_entry.pack()

        def on_add_face():
            name = name_entry.get()
            if name:
                add_new_face(name)
                new_window.destroy()
            else:
                print("Lütfen bir isim girin.")

        ttk.Button(new_window, text="Kaydet", command=on_add_face).pack()

    def on_mouse_down(self, event):
        global entry_zone_top_left, drawing
        drawing = True
        entry_zone_top_left = (event.x, event.y)

    def on_mouse_move(self, event):
        global entry_zone_bottom_right
        if drawing:
            entry_zone_bottom_right = (event.x, event.y)

    def on_mouse_up(self, event):
        global drawing
        drawing = False

    def update_video(self):
        ret, frame = cap.read()
        if not ret:
            self.root.after(10, self.update_video)
            return

        # İzinsiz giriş alanını çizin
        if entry_zone_top_left and entry_zone_bottom_right:
            cv2.rectangle(frame, entry_zone_top_left, entry_zone_bottom_right, (0, 255, 0), 2)

        # Video gösterim alanını güncelle
        frame = cv2.resize(frame, (640, 480))
        annotated_frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(annotated_frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # 10ms sonra güncelle
        self.root.after(10, self.update_video)

    def process_frames(self):
        while camera_open:
            ret, frame = cap.read()
            if not ret:
                continue

            # Modeli frame üzerinde çalıştırın
            results = model(frame)

            # Tespit edilen nesnelerle frame'i alın
            annotated_frame = frame.copy()

            # Tespit edilen nesneleri kontrol edin
            for result in results[0].boxes:
                if int(result.cls) == 0:  # 'person' sınıfı
                    x1, y1, x2, y2 = map(int, result.xyxy[0])  # Tensor'dan koordinatları al
                    person_area = calculate_area(x1, y1, x2, y2)
                    if entry_zone_top_left and entry_zone_bottom_right:
                        intersection_area = calculate_intersection_area((x1, y1, x2, y2),
                                                                        (entry_zone_top_left[0], entry_zone_top_left[1],
                                                                         entry_zone_bottom_right[0], entry_zone_bottom_right[1]))

                        if intersection_area >= 0.6 * person_area:
                            # İzinsiz giriş tespit edildi, yüzü algıla
                            face_frame = frame[y1:y2, x1:x2]
                            rgb_face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)
                            face_locations = face_recognition.face_locations(rgb_face_frame)
                            face_encodings = face_recognition.face_encodings(rgb_face_frame, face_locations)

                            unauthorized_entry = False
                            for face_encoding, face_location in zip(face_encodings, face_locations):
                                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                                best_match_index = np.argmin(face_distances)

                                if matches[best_match_index]:
                                    name = known_face_names[best_match_index]
                                    if name not in recognized_names:
                                        recognized_names.add(name)
                                        self.log_text.insert(tk.END, f"{datetime.now()}: Yüz algılandı: {name}\n")
                                else:
                                    unauthorized_entry = True
                                    if not alarm_triggered:
                                        self.trigger_alarm()
                                    # Tanınmayan yüz, güvenlik uyarısı gönder
                                    person_image_path = 'izinsizgiriş_kişi.jpg'
                                    cv2.imwrite(person_image_path, frame)
                                    print("send_email işlevi çağrılıyor.")
                                    send_email(person_image_path)
                                    self.log_text.insert(tk.END, f"{datetime.now()}: Güvenlik uyarısı! Yetkisiz giriş tespit edildi.\n")

                            if not unauthorized_entry:
                                # Tanınmayan yüz yoksa döngüyü kırın
                                break
            time.sleep(0.1)

    def trigger_alarm(self):
        global alarm_triggered, send_email_flag
        alarm_triggered = True
        send_email_flag = True  # Bu satırı True olarak değiştiriyoruz
        pygame.mixer.music.play()
        self.log_text.insert(tk.END, f"{datetime.now()}: Alarm tetiklendi!\n")
        print("Alarm tetiklendi. send_email_flag True olarak ayarlandı.")

    def reset_alarm(self):
        global alarm_triggered, send_email_flag
        alarm_triggered = False
        send_email_flag = False
        pygame.mixer.music.stop()
        self.log_text.insert(tk.END, f"{datetime.now()}: Alarm sıfırlama.\n")
        print("Alarm sıfırlama. send_email_flag Yanlış olarak ayarlandı.")

# Kamera açma ve arayüzü başlatma
cap = cv2.VideoCapture(0)
root = tk.Tk()
app = SecurityApp(root)
root.mainloop()

# Kamerayı kapatın
cap.release()
cv2.destroyAllWindows()
