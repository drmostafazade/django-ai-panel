import os
import django
from django.test import Client
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# ایجاد client تست
client = Client()

# گرفتن یا ایجاد کاربر
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@bsepar.com', 'is_staff': True, 'is_superuser': True}
)
if created:
    user.set_password('test123456')
    user.save()
    print(f"✅ User created: {user.username}")
else:
    print(f"✅ User exists: {user.username}")

# ورود کاربر
client.force_login(user)

# تست صفحه settings
try:
    response = client.get('/ai-chat/settings/')
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode()
        
        # چک کردن وجود دکمه‌های جدید
        if 'btn-balance' in content:
            print("✅ btn-balance found!")
        else:
            print("❌ btn-balance NOT found")
            
        if 'action-btn' in content:
            print("✅ action-btn found!")
        else:
            print("❌ action-btn NOT found")
            
        if 'btn-personal' in content:
            print("✅ btn-personal found!")
        else:
            print("❌ btn-personal NOT found")
            
        # نمایش بخشی از محتوا
        if 'table-actions' in content:
            print("✅ table-actions found!")
        else:
            print("❌ table-actions NOT found")
            
        print(f"\nContent length: {len(content)} characters")
        
        # ذخیره محتوا برای بررسی
        with open('/tmp/api_settings_response.html', 'w') as f:
            f.write(content)
        print("📄 Response saved to /tmp/api_settings_response.html")
        
    else:
        print(f"❌ Error: Status {response.status_code}")
        print(response.content.decode()[:500])
        
except Exception as e:
    print(f"❌ Exception: {e}")
