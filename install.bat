@echo off
title نظام إدارة المستندات - التثبيت
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║           نظام إدارة المستندات - التثبيت التلقائي         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM التحقق من Python
echo [1/7] التحقق من Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo ❌ خطأ: Python غير مثبت!
    echo.
    echo 📥 قم بتثبيت Python من:
    echo    https://www.python.org/downloads/
    echo.
    echo ⚠️  مهم: ضع علامة على "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
echo ✅ Python موجود
echo.

REM إنشاء البيئة الافتراضية
echo [2/7] إنشاء البيئة الافتراضية...
if exist venv (
    echo ℹ️  البيئة موجودة مسبقاً، سيتم استخدامها
) else (
    python -m venv venv
    echo ✅ تم إنشاء البيئة
)
echo.

REM تفعيل البيئة
echo [3/7] تفعيل البيئة...
call venv\Scripts\activate.bat
echo ✅ تم التفعيل
echo.

REM تثبيت المكتبات
echo [4/7] تثبيت المكتبات... (قد يستغرق 3-5 دقائق)
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if errorlevel 1 (
    color 0C
    echo ❌ فشل تثبيت المكتبات
    pause
    exit /b 1
)
echo ✅ تم تثبيت المكتبات
echo.

REM إعداد ملف .env
echo [5/7] إعداد الإعدادات...
if not exist .env (
    copy .env.example .env >nul
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > temp_key.txt
    set /p NEW_SECRET_KEY=<temp_key.txt
    del temp_key.txt
    powershell -Command "(gc .env) -replace 'your-secret-key-here-change-in-production', '%NEW_SECRET_KEY%' | Out-File -encoding ASCII .env" >nul
    echo ✅ تم إنشاء ملف الإعدادات
) else (
    echo ℹ️  ملف الإعدادات موجود
)
echo.

REM إنشاء المجلدات
echo [6/7] إنشاء المجلدات...
if not exist media\documents mkdir media\documents
if not exist logs mkdir logs
if not exist staticfiles mkdir staticfiles
if not exist backups mkdir backups
echo ✅ تم إنشاء المجلدات
echo.

REM إعداد قاعدة البيانات
echo [7/7] إعداد قاعدة البيانات...
python manage.py makemigrations >nul 2>&1
python manage.py migrate >nul 2>&1
python manage.py collectstatic --noinput >nul 2>&1
echo ✅ تم إعداد قاعدة البيانات
echo.

REM إنشاء superuser
echo ════════════════════════════════════════════════════════════════
echo.
echo 👤 الآن سنقوم بإنشاء حساب المدير الرئيسي
echo.
echo ⚠️  احفظ هذه المعلومات في مكان آمن!
echo.
echo ════════════════════════════════════════════════════════════════
echo.
python manage.py createsuperuser --username admin --email admin@company.com
echo.

REM إعداد المجموعات
echo ════════════════════════════════════════════════════════════════
echo إعداد الصلاحيات والمجموعات...
python setup.py
echo.

REM النتيجة النهائية
color 0A
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ✅ اكتمل التثبيت بنجاح! ✅                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 لتشغيل النظام:
echo    ضاعف كليك على: run.bat
echo.
echo 🌐 بعد التشغيل افتح المتصفح:
echo    http://localhost:8000
echo.
echo 👤 معلومات تسجيل الدخول:
echo    Username: admin
echo    Password: (كلمة المرور التي أدخلتها للتو)
echo.
echo 📝 حسابات تجريبية متاحة:
echo    employee1 / emp123
echo    employee2 / emp123
echo.
echo ════════════════════════════════════════════════════════════════
echo.
pause