#!/usr/bin/env python3
import os
import sys
import datetime
import glob
import subprocess
import json

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip(),
            'returncode': result.returncode
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def check_file_content(filepath, search_terms):
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            results = {}
            for term in search_terms:
                results[term] = term in content
            
            return {
                'exists': True,
                'size': len(content),
                'lines': len(content.split('\n')),
                'search_results': results,
                'sample': content[:200] + '...' if len(content) > 200 else content
            }
        else:
            return {'exists': False}
    except Exception as e:
        return {'exists': False, 'error': str(e)}

def main():
    print("=" * 80)
    print("🔍 BSEPAR PANEL - SYSTEM ANALYSIS REPORT")
    print(f"📅 Generated: {datetime.datetime.now()}")
    print("=" * 80)
    
    # 1. بررسی محیط پایه
    print("\n1️⃣ BASE ENVIRONMENT")
    print("-" * 50)
    
    # مسیر فعلی
    current_dir = os.getcwd()
    print(f"📂 Current Directory: {current_dir}")
    
    # بررسی Python و Django
    python_version = run_command("python3 --version")
    print(f"🐍 Python Version: {python_version['stdout']}")
    
    # بررسی virtual environment
    venv_active = os.environ.get('VIRTUAL_ENV')
    print(f"🔧 Virtual Environment: {venv_active if venv_active else 'Not Active'}")
    
    # بررسی Django
    django_check = run_command("cd /var/www/bsepar_panel && source venv/bin/activate && python manage.py check")
    print(f"⚙️ Django Check: {'✅ OK' if django_check['success'] else '❌ ERROR'}")
    if not django_check['success']:
        print(f"   Error: {django_check['stderr']}")
    
    # 2. بررسی ساختار پروژه
    print("\n2️⃣ PROJECT STRUCTURE")
    print("-" * 50)
    
    base_path = "/var/www/bsepar_panel"
    
    # ساختار کلی
    for root, dirs, files in os.walk(base_path):
        # محدود کردن عمق
        level = root.replace(base_path, '').count(os.sep)
        if level < 3:
            indent = ' ' * 2 * level
            print(f"{indent}📁 {os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # نمایش 5 فایل اول
                print(f"{subindent}📄 {file}")
            if len(files) > 5:
                print(f"{subindent}... and {len(files) - 5} more files")
    
    # 3. بررسی فایل‌های مهم Django
    print("\n3️⃣ DJANGO CONFIGURATION FILES")
    print("-" * 50)
    
    important_files = {
        'settings.py': '/var/www/bsepar_panel/config/settings.py',
        'main_urls.py': '/var/www/bsepar_panel/config/urls.py',
        'ai_manager_urls.py': '/var/www/bsepar_panel/ai_manager/urls.py',
        'ai_manager_views.py': '/var/www/bsepar_panel/ai_manager/views.py',
        'ai_manager_models.py': '/var/www/bsepar_panel/ai_manager/models.py',
    }
    
    for name, filepath in important_files.items():
        if os.path.exists(filepath):
            stat = os.stat(filepath)
            print(f"✅ {name}: {filepath}")
            print(f"   📊 Size: {stat.st_size} bytes, Modified: {datetime.datetime.fromtimestamp(stat.st_mtime)}")
        else:
            print(f"❌ {name}: NOT FOUND at {filepath}")
    
    # 4. بررسی Templates
    print("\n4️⃣ TEMPLATE FILES")
    print("-" * 50)
    
    # پیدا کردن همه فایل‌های template
    template_patterns = [
        '/var/www/bsepar_panel/**/api_settings*.html',
        '/var/www/bsepar_panel/**/templates/**/*.html'
    ]
    
    all_templates = []
    for pattern in template_patterns:
        all_templates.extend(glob.glob(pattern, recursive=True))
    
    # حذف تکراری‌ها
    all_templates = list(set(all_templates))
    
    print(f"📄 Found {len(all_templates)} template files:")
    for template in sorted(all_templates):
        if 'api_settings' in template or 'ai' in template.lower():
            stat = os.stat(template)
            print(f"   📄 {template}")
            print(f"      Size: {stat.st_size} bytes, Modified: {datetime.datetime.fromtimestamp(stat.st_mtime)}")
            
            # چک کردن محتوای مهم
            search_terms = ['btn-balance', 'action-btn', 'btn-personal', 'table-actions']
            content_check = check_file_content(template, search_terms)
            if content_check['exists']:
                found_terms = [term for term, found in content_check['search_results'].items() if found]
                if found_terms:
                    print(f"      🎯 Contains: {', '.join(found_terms)}")
                else:
                    print(f"      ⚠️ No target CSS classes found")
    
    # 5. بررسی URL Patterns
    print("\n5️⃣ URL CONFIGURATION")
    print("-" * 50)
    
    # خواندن main urls
    main_urls_content = check_file_content('/var/www/bsepar_panel/config/urls.py', [])
    if main_urls_content['exists']:
        print("📋 Main URLs (config/urls.py):")
        print("   " + main_urls_content['sample'].replace('\n', '\n   '))
    
    # خواندن ai_manager urls
    ai_urls_content = check_file_content('/var/www/bsepar_panel/ai_manager/urls.py', [])
    if ai_urls_content['exists']:
        print("\n📋 AI Manager URLs (ai_manager/urls.py):")
        print("   " + ai_urls_content['sample'].replace('\n', '\n   '))
    
    # 6. بررسی Static Files
    print("\n6️⃣ STATIC FILES")
    print("-" * 50)
    
    static_dirs = [
        '/var/www/bsepar_panel/static/',
        '/var/www/bsepar_panel/staticfiles/',
        '/var/www/bsepar_panel/ai_manager/static/'
    ]
    
    for static_dir in static_dirs:
        if os.path.exists(static_dir):
            files = glob.glob(f"{static_dir}**/*", recursive=True)
            print(f"📁 {static_dir}: {len([f for f in files if os.path.isfile(f)])} files")
        else:
            print(f"❌ {static_dir}: NOT FOUND")
    
    # 7. بررسی Services
    print("\n7️⃣ SYSTEM SERVICES")
    print("-" * 50)
    
    services = ['gunicorn_bsepar_panel', 'nginx']
    for service in services:
        status = run_command(f"systemctl is-active {service}")
        print(f"🔧 {service}: {status['stdout']}")
        
        if service == 'gunicorn_bsepar_panel':
            # گرفتن لاگ‌های اخیر
            logs = run_command(f"journalctl -u {service} --since '10 minutes ago' --no-pager -q")
            if logs['stdout']:
                print(f"   📋 Recent logs (last 10 mins):")
                for line in logs['stdout'].split('\n')[-5:]:
                    if line.strip():
                        print(f"      {line}")
    
    # 8. بررسی Nginx Configuration
    print("\n8️⃣ NGINX CONFIGURATION")
    print("-" * 50)
    
    nginx_config = check_file_content('/etc/nginx/conf.d/bsepar_panel.conf', [])
    if nginx_config['exists']:
        print("📋 Nginx Config:")
        print("   " + nginx_config['sample'].replace('\n', '\n   '))
    
    # 9. بررسی Database
    print("\n9️⃣ DATABASE")
    print("-" * 50)
    
    db_check = run_command("cd /var/www/bsepar_panel && source venv/bin/activate && python manage.py showmigrations")
    if db_check['success']:
        print("✅ Database migrations:")
        for line in db_check['stdout'].split('\n')[:10]:
            if line.strip():
                print(f"   {line}")
    else:
        print(f"❌ Database check failed: {db_check['stderr']}")
    
    # 10. تست URL های موجود
    print("\n🔟 URL TESTING")
    print("-" * 50)
    
    test_urls = [
        'https://panel.bsepar.com/',
        'https://panel.bsepar.com/login/',
        'https://panel.bsepar.com/ai-chat/',
        'https://panel.bsepar.com/ai-chat/settings/',
    ]
    
    for url in test_urls:
        curl_result = run_command(f"curl -s -o /dev/null -w '%{{http_code}}' '{url}'")
        print(f"🌐 {url}: HTTP {curl_result['stdout']}")
    
    # 11. خلاصه نهایی
    print("\n" + "=" * 80)
    print("📊 SUMMARY & RECOMMENDATIONS")
    print("=" * 80)
    
    print("\n🔍 Key Findings:")
    
    # چک کردن مشکلات احتمالی
    issues = []
    
    if not django_check['success']:
        issues.append("❌ Django configuration has issues")
    
    if not venv_active:
        issues.append("⚠️ Virtual environment not detected")
    
    # چک کردن template ها
    template_with_buttons = False
    for template in all_templates:
        if 'api_settings' in template:
            content_check = check_file_content(template, ['btn-balance'])
            if content_check['exists'] and content_check['search_results'].get('btn-balance', False):
                template_with_buttons = True
                print(f"✅ Found template with new buttons: {template}")
                break
    
    if not template_with_buttons:
        issues.append("❌ No template found with new button styles")
    
    if issues:
        print("\n🚨 Issues Found:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("\n✅ No major issues detected!")
    
    print(f"\n📅 Report completed at: {datetime.datetime.now()}")
    print("💾 This report has been saved for further analysis")

if __name__ == "__main__":
    main()
