# 📱 HM Video Downloader

![Giriş Ekranı](screenshots/login.png)
![Ana Sayfa](screenshots/main_screen.png)
![Yan Menü](screenshots/drawer.png)
![İndirme Listesi](screenshots/downloads.png)

**HM Video Downloader** uygulaması, **YouTube**, **Instagram**, **Facebook** ve **Twitter** gibi popüler platformlardan **video indirmek** için tasarlanmıştır.

---

## 🔧 Kullanılan Teknolojiler

- **Dil:** Dart (Flutter tabanlı)
- **Harici API’ler:** Videoların doğrudan bağlantılarını almak için
- **UI/UX:** Flutter Material Bileşenleri, özel widget’lar
- **Kütüphaneler:**
  - `dio`, `http`, `video_thumbnail`
  - `chewie`, `equatable`, `path_provider` ve diğerleri

---

## ✅ Temel Özellikler

- 📥 Video indirme desteği:
  - YouTube
  - Instagram
  - Twitter
  - Facebook
- İndirme öncesi kalite seçimi
- İndirme durumu takibi
- Splash ekran, giriş sayfası, logolu Drawer, özel kullanıcı arayüzü
- **Karanlık ve aydınlık tema** desteği
- İndirilen videoların listelenmesi

---

## ⚠ Dikkat Edilmesi Gerekenler

### 🔗 Linkleri nereden kopyalamalıyım?

> **Linkler sadece resmi uygulamalardan kopyalanmalıdır** (Instagram, YouTube, Facebook, Twitter).  
> Google veya Yandex gibi tarayıcılardan kopyalanan linkler **geçersiz** olabilir ve uygulama tarafından tanınmaz.

### 📂 Neden indirilen videolar oynatılamıyor?

> Bu bir **hata değildir**. İndirilen videolar **cihazın yerel hafızasında** saklanır.  
> Android Studio emülatörleri ile çalışırken bu videolar oynatılamayabilir — bu durum emülatörlerin dosya sisteminden kaynaklanmaktadır.  
> **Gerçek cihazlarda** videolar sorunsuz bir şekilde indirilmektedir ve manuel olarak açılabilir.

---

## 💡 Uygulamanın Çalıştırılması

1. Projeyi bir klasöre çıkarın.
2. Android Studio veya VSCode ile açın.
3. `Pub get` çalıştırarak bağımlılıkları yükleyin.
4. Emülatörde veya bağlı cihazda uygulamayı başlatın.

---

## 👨‍💻 Geliştirici Bilgileri

- Proje **tek kişi** tarafından geliştirilmiştir — **Abdurahman Kaıbaliev - 030721109**
- Tüm bileşenler elle yazılmıştır: UI, indirme mantığı, API entegrasyonu
- **Clean Architecture** mimarisi kullanılmıştır:
  - `data`, `domain`, `presentation` katmanları
- Sayfa yönlendirmeleri `main.dart` üzerinden yapılmıştır

---
