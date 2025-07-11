# پنل توسعه هوشمند بسپار

## 🚀 نصب و راه‌اندازی

این پروژه یک پنل توسعه هوشمند با Django است که امکان مدیریت پروژه‌های GitHub را فراهم می‌کند.

### پیش‌نیازها
- Python 3.12+
- PostgreSQL 16
- Nginx
- Git

### نصب

git clone https://github.com/drmostafazade/django-ai-panel.git
cd django-ai-panel
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
تنظیمات

فایل config/db_settings.py را با اطلاعات دیتابیس خود تنظیم کنید
python manage.py migrate را اجرا کنید
python manage.py createsuperuser برای ایجاد کاربر ادمین
python manage.py collectstatic برای جمع‌آوری فایل‌های استاتیک

اجرا
gunicorn config.wsgi:application --bind unix:/path/to/gunicorn.sock
📋 ویژگی‌ها

✅ سیستم احراز هویت کامل
✅ مدیریت توکن GitHub
✅ همگام‌سازی و مدیریت مخازن
✅ رابط کاربری فارسی و RTL
✅ طراحی مشابه Django Admin

🛠️ تکنولوژی‌ها

Django 5.0.1
PostgreSQL 16
Python 3.12
Gunicorn + Nginx

📝 مستندات

PROGRESS.md - پیشرفت پروژه
CURRENT_STATUS.md - وضعیت فعلی
CHANGELOG.md - تاریخچه تغییرات

👤 توسعه‌دهنده
Dr. Mostafazade - GitHub
📄 لایسنس
MIT License
