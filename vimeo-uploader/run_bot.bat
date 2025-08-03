@echo off
chcp 65001 >nul
title نظام رفع الفيديوهات من تليجرام إلى فيمو

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    نظام رفع الفيديوهات                        ║
echo ║                من تليجرام إلى فيمو 📹🤖                      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 التحقق من Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت أو غير موجود في PATH
    echo 💡 قم بتحميل Python من https://python.org
    pause
    exit /b 1
)

echo ✅ Python مثبت
echo.

if not exist ".env" (
    echo ❌ ملف .env غير موجود
    echo 💡 قم بتشغيل: python setup.py
    pause
    exit /b 1
)

echo 🤖 بدء تشغيل البوت...
echo.
echo 💡 لإيقاف البوت، اضغط Ctrl+C
echo.

python run_bot.py

echo.
echo 🛑 تم إيقاف البوت
pause