# ساختار پروژه پنل توسعه هوشمند
bsepar_panel/
├── config/              # تنظیمات Django
│   ├── init.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                # اپ هسته (احراز هویت)
│   ├── init.py
│   ├── auth_views.py
│   ├── urls.py
│   └── views.py
├── dashboard/           # داشبورد اصلی
│   ├── init.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   └── views.py
├── ai_manager/          # مدیریت API های AI
├── terminal_manager/    # ترمینال SSH
├── git_manager/         # عملیات Git
├── project_manager/     # مدیریت پروژه‌ها
├── voice_manager/       # ورودی صوتی
├── log_analyzer/        # تحلیل لاگ
├── knowledge_base/      # سیستم یادگیری
├── webhook_handler/     # وب‌هوک‌ها
├── monitoring/          # مانیتورینگ
├── templates/           # قالب‌های HTML
│   ├── base/
│   │   └── base.html
│   ├── auth/
│   │   └── login.html
│   └── dashboard/
│       └── home.html
├── static/              # فایل‌های استاتیک
│   ├── css/
│   ├── js/
│   └── img/
├── reports/             # گزارشات
│   └── weekly/
├── venv/                # محیط مجازی
├── manage.py            # مدیریت Django
├── requirements.txt     # پکیج‌های Python
├── .env                 # متغیرهای محیطی
├── .gitignore          # فایل‌های نادیده گرفته شده
├── README.md           # راهنمای پروژه
├── PROGRESS.md         # سند پیشرفت
├── CURRENT_STATUS.md   # وضعیت فعلی
└── DAILY_REPORT.md     # گزارش روزانه
