# 💼 Davranış Tabanlı Prim Önericisi

Bu proje, çalışanların anket yanıtlarına dayalı olarak prim önerisi sunan bir web uygulamasıdır. Flask tabanlı bu sistemde kullanıcılar anket doldurur, sonuçlara göre prim önerisi alır ve tüm bilgiler veritabanında saklanır. Ayrıca bir yönetici paneli mevcuttur.

---

## 🚀 Özellikler

- 👤 Kullanıcı Kayıt ve Giriş Sistemi
- 📋 Anket Formu (Kullanıcı senaryolarına dayalı sorular)
- 🎯 Prim Hesaplama ve Önerme
- 📊 Kullanıcı Profil Sayfası (Geçmiş sonuçları görüntüleme + şifre değiştirme)
- 🛠️ Admin Paneli (Kullanıcı arama + geçmiş sonuçları görüntüleme)
- 📱 Mobil uyumlu ve modern tasarım (Bootstrap ile)
- 🌐 Deploy: [https://prim-onerici.onrender.com](https://prim-onerici.onrender.com)

---

## ⚙️ Kullanılan Teknolojiler

- Backend: Flask (Python)
- Frontend: HTML, Bootstrap, Jinja2
- Veritabanı: SQLite
- Hosting: Render
- Diğer: Flask-Login, SQLAlchemy, Logging

---

## 🧪 Kurulum

1. Projeyi klonlayın:

```bash
git clone https://github.com/ulysn/prim_onerici.git
cd prim_onerici

2. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt

3. Veritabanını oluşturun:

```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()

4. Uygulamayı çalıştırın:

```bash
python app.py

-👩‍💼 Admin Paneli

Admin kullanıcılar özel bir panelden kullanıcıları arayabilir ve onların anket geçmişini görebilir.

-🔒 Notlar

* Şifreler hash'lenmiş olarak saklanır.

* Oturum yönetimi Flask-Login ile sağlanır.

* Geliştirme modunda çalışmaktadır; canlı sistem için WSGI kurulumu gereklidir

✨ Geliştiren

Elif Bilge Yavuz
Software Engineering Undergraduate student – EMU
GitHub: @ulysn