# تغییرات احراز هویت PostgreSQL

## مشکل
PostgreSQL 16 از `scram-sha-256` به جای `md5` استفاده می‌کند که امن‌تر است.
Odoo این تغییر را اعمال کرده و pg_hba.conf را تغییر داده است.

## تنظیمات فعلی
local   all   all   scram-sha-256
host    all   all   127.0.0.1/32   scram-sha-256
## راه حل
1. تنظیم رمز عبور با الگوریتم صحیح
2. اطمینان از استفاده psycopg2 از scram-sha-256

## نکته مهم
هرگز به md5 برنگردید چون امنیت کمتری دارد.
