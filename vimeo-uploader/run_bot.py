#!/usr/bin/env python3
"""
ملف تشغيل سريع لبوت رفع الفيديوهات
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """التحقق من المتطلبات"""
    print("🔍 التحقق من المتطلبات...")
    
    # التحقق من ملف .env
    if not Path(".env").exists():
        print("❌ ملف .env غير موجود")
        print("💡 قم بتشغيل: python setup.py")
        return False
    
    # التحقق من ملف teachers.json
    if not Path("teachers.json").exists():
        print("⚠️ ملف teachers.json غير موجود")
        print("💡 سيتم إنشاؤه تلقائياً")
    
    return True

def main():
    """تشغيل البوت"""
    print("🤖 بدء تشغيل بوت رفع الفيديوهات...")
    
    # التحقق من المتطلبات
    if not check_requirements():
        return
    
    try:
        # تشغيل البوت
        from telegram_bot import main as run_bot
        run_bot()
    except KeyboardInterrupt:
        print("\n\n🛑 تم إيقاف البوت")
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل البوت: {e}")
        print("💡 تأكد من صحة البيانات في ملف .env")

if __name__ == "__main__":
    main()