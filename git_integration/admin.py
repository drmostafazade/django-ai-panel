from django.contrib import admin
from .models import GitHubToken, Repository

# تنظیمات سایت
admin.site.site_header = "پنل توسعه هوشمند بسپار"
admin.site.site_title = "پنل بسپار"
admin.site.index_title = "خوش آمدید"

# ثبت مدل‌ها به صورت ساده
admin.site.register(GitHubToken)
admin.site.register(Repository)
