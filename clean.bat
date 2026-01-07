@echo off
echo جاري تنظيف المشروع...

REM حذف البيئة الافتراضية
if exist venv rmdir /s /q venv

REM حذف قاعدة البيانات
if exist db.sqlite3 del db.sqlite3

REM حذف ملفات Python المؤقتة
for /r %%i in (__pycache__) do @if exist "%%i" rmdir /s /q "%%i"
for /r %%i in (*.pyc) do @if exist "%%i" del "%%i"

REM حذف migrations (احتفظ بـ __init__.py)
del /s /q accounts\migrations\*.py 2>nul
del /s /q documents\migrations\*.py 2>nul
echo. > accounts\migrations\__init__.py
echo. > documents\migrations\__init__.py

REM حذف static files المجمعة
if exist staticfiles rmdir /s /q staticfiles

REM حذف logs
if exist logs\*.log del /q logs\*.log

echo تم التنظيف بنجاح!
pause