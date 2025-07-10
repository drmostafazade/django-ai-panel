# پنل توسعه هوشمند بسپار

🌐 **آدرس**: https://panel.bsepar.com

## معرفی
پلتفرم جامع مدیریت توسعه نرم‌افزار با استفاده از هوش مصنوعی

## ویژگی‌ها
- 🤖 یکپارچگی با چندین AI
- 💻 ترمینال SSH تحت وب
- 🔄 مدیریت خودکار Git
- 🧠 سیستم یادگیری از تجربیات
- 🇮🇷 پشتیبانی کامل زبان فارسی

## مستندات
- [PROGRESS.md](PROGRESS.md) - سند پیشرفت پروژه
- [CURRENT_STATUS.md](CURRENT_STATUS.md) - وضعیت فعلی

## 🛠️ نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.10+
- PostgreSQL 15+
- Redis
- Nginx

### مراحل نصب

cd /var/www/bsepar_panel
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
bsepar_panel/
├── ai_manager/          # مدیریت API های AI
├── terminal_manager/    # ترمینال SSH
├── dashboard/           # داشبورد اصلی
├── knowledge_base/      # سیستم یادگیری
└── ...
🔄 وضعیت توسعه

فاز 1: در حال انجام (30%)
CURRENT_STATUS.md را برای جزئیات ببینید
