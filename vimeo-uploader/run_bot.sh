#!/bin/bash

# نظام رفع الفيديوهات من تليجرام إلى فيمو

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    نظام رفع الفيديوهات                        ║"
echo "║                من تليجرام إلى فيمو 📹🤖                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

echo "🔍 التحقق من Python..."

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python غير مثبت"
        echo "💡 قم بتثبيت Python من https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python مثبت"
echo ""

# التحقق من ملف .env
if [ ! -f ".env" ]; then
    echo "❌ ملف .env غير موجود"
    echo "💡 قم بتشغيل: $PYTHON_CMD setup.py"
    exit 1
fi

echo "🤖 بدء تشغيل البوت..."
echo ""
echo "💡 لإيقاف البوت، اضغط Ctrl+C"
echo ""

# تشغيل البوت
$PYTHON_CMD run_bot.py

echo ""
echo "🛑 تم إيقاف البوت"