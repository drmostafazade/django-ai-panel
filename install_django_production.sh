#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# --- متغیرهای پروژه ---
DOMAIN="panel.bsepar.com"
PROJECT_NAME="bsepar_panel"
REPO_URL="https://github.com/drmostafazade/django.git"
PROJECT_DIR="/var/www/bsepar_panel"
DB_NAME="bsepar_panel_db"
DB_USER="bsepar_panel_user"
DB_PASS=$(openssl rand -base64 24)
RUN_USER="www-data"

# مسیر جدید و امن برای سوکت
SOCKET_PATH="$PROJECT_DIR/gunicorn.sock"

# --- مسیر ذخیره‌سازی فایل‌های SSL ---
SSL_DIR="/etc/nginx/ssl/$DOMAIN"
SSL_KEY_FILE="$SSL_DIR/privkey.key"
SSL_CERT_FILE="$SSL_DIR/combined_chain.pem"

# ==============================================================================
# >>> مرحله 1: دریافت 3 قطعه کلید و گواهی SSL <<<
# ==============================================================================

echo "================================================================="
echo "        راه اندازی SSL برای دامنه $DOMAIN (روش Ctrl+D)"
echo "================================================================="

function get_input() {
    local prompt_message=$1
    echo -e "\n>>> ${prompt_message}"
    echo ">>> پس از پیست کردن، کلیدهای Ctrl+D را همزمان فشار دهید."
    cat
}

PRIVATE_KEY_CONTENT=$(get_input "1/3: لطفاً محتوای کامل و صحیح کلید خصوصی (Private Key) را پیست کنید.")
if [ -z "$PRIVATE_KEY_CONTENT" ]; then echo "خطا: کلید خصوصی وارد نشد." && exit 1; fi
read -p "آیا کلید خصوصی به درستی وارد شد؟ (y/n): " -r confirm < /dev/tty
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then echo "عملیات لغو شد." && exit 1; fi

CERT_CONTENT=$(get_input "2/3: لطفاً محتوای کامل و صحیح گواهی اصلی (Certificate) را پیست کنید.")
if [ -z "$CERT_CONTENT" ]; then echo "خطا: گواهی اصلی وارد نشد." && exit 1; fi
read -p "آیا گواهی اصلی به درستی وارد شد؟ (y/n): " -r confirm < /dev/tty
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then echo "عملیات لغو شد." && exit 1; fi

CA_BUNDLE_CONTENT=$(get_input "3/3: لطفاً محتوای کامل و صحیح گواهی واسط (CA Bundle) را پیست کنید.")
if [ -z "$CA_BUNDLE_CONTENT" ]; then echo "خطا: گواهی واسط وارد نشد." && exit 1; fi
read -p "آیا گواهی واسط به درستی وارد شد؟ (y/n): " -r confirm < /dev/tty
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then echo "عملیات لغو شد." && exit 1; fi

echo -e "\n✓ اطلاعات SSL با موفقیت دریافت شد. شروع فرآیند نصب..."

# ==============================================================================
# >>> مرحله 2: نصب و پیکربندی خودکار <<<
# ==============================================================================

PG_VERSION=$(ls /etc/postgresql/)
PG_HBA_FILE="/etc/postgresql/${PG_VERSION}/main/pg_hba.conf"
echo ">>> اصلاح فایل $PG_HBA_FILE برای فعال‌سازی احراز هویت با رمز عبور..."
sudo sed -i -E "s/^(local\s+all\s+all\s+).*/\1scram-sha-256/" "$PG_HBA_FILE"
sudo sed -i -E "s/^(host\s+all\s+all\s+127\.0\.0\.1\/32\s+).*/\1scram-sha-256/" "$PG_HBA_FILE"
sudo systemctl restart postgresql

# **FIX:** بازسازی صحیح فایل‌های SSL
echo ">>> ایجاد و بازسازی فایل‌های SSL..."
sudo mkdir -p "$SSL_DIR"
echo -e "$PRIVATE_KEY_CONTENT" | sudo tee "$SSL_KEY_FILE" > /dev/null
# **FIX:** اطمینان از وجود یک خط جدید بین دو گواهی برای جلوگیری از خطای PEM
{ echo -e "$CERT_CONTENT"; echo; echo -e "$CA_BUNDLE_CONTENT"; } | sudo tee "$SSL_CERT_FILE" > /dev/null
sudo chmod 600 "$SSL_KEY_FILE"
echo "✓ فایل‌های SSL به صورت امن در مسیر $SSL_DIR ذخیره شدند."

sudo apt-get update > /dev/null && sudo apt-get install -y gunicorn

echo ">>> ایجاد دیتابیس و کاربر در PostgreSQL..."
if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
    sudo -u postgres psql --command "CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASS';" > /dev/null
else
    sudo -u postgres psql --command "ALTER USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASS';" > /dev/null
fi
if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    sudo -u postgres psql --command "CREATE DATABASE $DB_NAME OWNER $DB_USER;" > /dev/null
fi
echo "✓ دیتابیس و کاربر با موفقیت ایجاد/آپدیت شد."

sudo mkdir -p $PROJECT_DIR
if [ ! -d "$PROJECT_DIR/.git" ]; then
    sudo git clone $REPO_URL $PROJECT_DIR
fi

sudo python3 -m venv $PROJECT_DIR/venv
sudo $PROJECT_DIR/venv/bin/pip install --upgrade pip > /dev/null
sudo $PROJECT_DIR/venv/bin/pip install django gunicorn psycopg2-binary > /dev/null

cd $PROJECT_DIR
if [ ! -f "$PROJECT_DIR/manage.py" ]; then
    sudo $PROJECT_DIR/venv/bin/django-admin startproject config .
    sudo $PROJECT_DIR/venv/bin/python manage.py startapp core
fi

SETTINGS_FILE="$PROJECT_DIR/config/settings.py"
sudo sed -i "s/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \['127.0.0.1', 'localhost', '$DOMAIN'\]/" $SETTINGS_FILE
sudo sed -i "/'ENGINE': 'django.db.backends.sqlite3',/c\ \ \ \ 'ENGINE': 'django.db.backends.postgresql'," $SETTINGS_FILE
sudo sed -i "/'NAME': BASE_DIR /c\ \ \ \ 'NAME': '$DB_NAME',\n\ \ \ \ 'USER': '$DB_USER',\n\ \ \ \ 'PASSWORD': '$DB_PASS',\n\ \ \ \ 'HOST': 'localhost',\n\ \ \ \ 'PORT': '5432'," $SETTINGS_FILE
if ! grep -q "'core'," "$SETTINGS_FILE"; then sudo sed -i "/'django.contrib.staticfiles',/a \ \ \ \ 'core'," $SETTINGS_FILE; fi
echo "STATIC_ROOT = BASE_DIR / 'staticfiles'" | sudo tee -a $SETTINGS_FILE > /dev/null

sudo tee "$PROJECT_DIR/core/views.py" > /dev/null <<'VIEW_EOF'
from django.http import HttpResponse
def hello_world(request): return HttpResponse("<h1>🎉 تبریک! نصب جنگو با موفقیت کامل شد. 🎉</h1>")
VIEW_EOF

sudo tee "$PROJECT_DIR/core/urls.py" > /dev/null <<'URLS_CORE_EOF'
from django.urls import path
from .views import hello_world
urlpatterns = [path('', hello_world, name='hello_world'),]
URLS_CORE_EOF

URLS_CONFIG_FILE="$PROJECT_DIR/config/urls.py"
sudo sed -i "s/from django.urls import path/from django.urls import path, include/" "$URLS_CONFIG_FILE"
if ! grep -q "path('', include('core.urls'))" "$URLS_CONFIG_FILE"; then sudo sed -i "/urlpatterns = \[/a \ \ \ \ path('', include('core.urls'))," "$URLS_CONFIG_FILE"; fi

sudo $PROJECT_DIR/venv/bin/python manage.py migrate
sudo $PROJECT_DIR/venv/bin/python manage.py collectstatic --noinput --clear
sudo chown -R $RUN_USER:$RUN_USER $PROJECT_DIR

echo ">>> ایجاد سرویس systemd برای Gunicorn..."
SERVICE_FILE="/etc/systemd/system/gunicorn_${PROJECT_NAME}.service"
sudo tee $SERVICE_FILE > /dev/null <<SERVICE_EOF
[Unit]
Description=gunicorn daemon for bsepar panel
After=network.target
[Service]
User=$RUN_USER
Group=$RUN_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --workers 3 --bind unix:$SOCKET_PATH config.wsgi:application
[Install]
WantedBy=multi-user.target
SERVICE_EOF

echo ">>> ایجاد فایل proxy_params..."
sudo tee /etc/nginx/proxy_params > /dev/null <<'PROXY_EOF'
proxy_set_header Host $http_host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
PROXY_EOF

echo ">>> پیکربندی Nginx با SSL..."
NGINX_CONF="/etc/nginx/conf.d/${PROJECT_NAME}.conf"
sudo tee $NGINX_CONF > /dev/null <<NGINX_EOF
server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$host\$request_uri;
}
server {
    listen 443 ssl http2;
    server_name $DOMAIN;
    ssl_certificate $SSL_CERT_FILE;
    ssl_certificate_key $SSL_KEY_FILE;
    location /static/ { alias $PROJECT_DIR/staticfiles/; }
    location / {
        include /etc/nginx/proxy_params;
        proxy_pass http://unix:$SOCKET_PATH;
    }
}
NGINX_EOF

echo ">>> راه‌اندازی نهایی سرویس‌ها..."
sudo systemctl daemon-reload
sudo systemctl enable gunicorn_${PROJECT_NAME}.service
sudo systemctl restart gunicorn_${PROJECT_NAME}.service
sudo nginx -t
sudo systemctl restart nginx

echo -e "\n================================================================="
echo "🎉 نصب با موفقیت کامل شد!"
echo -e "\nآدرس سایت شما: https://$DOMAIN"
echo -e "\nاطلاعات دیتابیس (برای ذخیره):"
echo "  - نام دیتابیس: $DB_NAME"
echo "  - نام کاربری:   $DB_USER"
echo "  - رمز عبور:     $DB_PASS"
echo "================================================================="

