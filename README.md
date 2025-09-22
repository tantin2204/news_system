# 📰 News System

Ứng dụng web tin tức đơn giản xây dựng bằng **Django + MySQL**.  
Cho phép người dùng duyệt tin, tìm kiếm, phân loại theo danh mục, và tác giả có thể đăng/sửa/xóa bài viết.  

---

## 🚀 Tính năng
- Xem danh sách tin tức theo danh mục.
- Tìm kiếm tin theo tiêu đề/nội dung.
- Đăng ký/đăng nhập người dùng.
- Tác giả có thể đăng, sửa, xóa bài viết.
- Quản trị qua Django Admin.

---

## ⚙️ Cài đặt
1. Clone repo
```bash
git clone https://github.com/tantin2204/news_system.git
cd news_system

2. Cài môi trường & thư viện
bash
Sao chép mã
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

3. Cấu hình database (MySQL)
Trong settings.py chỉnh lại thông tin DB:

python
Sao chép mã
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'news_db',
        'USER': 'news_user',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

4. Chạy migrate & tạo superuser
bash
Sao chép mã
python manage.py migrate
python manage.py createsuperuser

5. Chạy server
bash
Sao chép mã
python manage.py runserver
Mở trình duyệt: http://localhost:8000

📂 Danh mục mẫu
Thời sự
Thể thao
Lao động
Kinh tế
Giải trí
Thời trang

👤 Demo account
Để đăng nhập thử hệ thống:
Admin:
  username: admin
  password: Ad@12345
Author:
  username: user1
  password: Tin@2204
Reader:
  username: user2
  password: Tin@2204

👨‍💻 Tác giả
Nguyễn Tấn Tín – GitHub

