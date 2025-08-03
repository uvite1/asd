#!/usr/bin/env python3
"""
ملف تجريبي لاختبار نظام رفع الفيديوهات
"""

import os
import sys
from pathlib import Path

def test_imports():
    """اختبار استيراد المكتبات"""
    print("🔍 اختبار استيراد المكتبات...")
    
    try:
        import flask
        print("✅ Flask - متوفر")
    except ImportError:
        print("❌ Flask - غير متوفر")
        return False
    
    try:
        import vimeo
        print("✅ PyVimeo - متوفر")
    except ImportError:
        print("❌ PyVimeo - غير متوفر")
        return False
    
    try:
        from telegram import Bot
        print("✅ python-telegram-bot - متوفر")
    except ImportError:
        print("❌ python-telegram-bot - غير متوفر")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv - متوفر")
    except ImportError:
        print("❌ python-dotenv - غير متوفر")
        return False
    
    return True

def test_files():
    """اختبار وجود الملفات المطلوبة"""
    print("\n📁 اختبار وجود الملفات...")
    
    required_files = [
        "telegram_bot.py",
        "teacher_manager.py",
        "app.py",
        "requirements.txt",
        ".env.example"
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} - موجود")
        else:
            print(f"❌ {file} - غير موجود")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_env_file():
    """اختبار ملف البيئة"""
    print("\n⚙️ اختبار ملف البيئة...")
    
    if not Path(".env").exists():
        print("⚠️ ملف .env غير موجود")
        print("💡 قم بتشغيل: python setup.py")
        return False
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # التحقق من المتغيرات المطلوبة
        required_vars = [
            "VIMEO_ACCESS_TOKEN",
            "VIMEO_CLIENT_ID", 
            "VIMEO_CLIENT_SECRET",
            "TELEGRAM_BOT_TOKEN"
        ]
        
        missing_vars = []
        for var in required_vars:
            value = os.getenv(var)
            if value and value != "YOUR_BOT_TOKEN_HERE":
                print(f"✅ {var} - محدد")
            else:
                print(f"❌ {var} - غير محدد")
                missing_vars.append(var)
        
        return len(missing_vars) == 0
        
    except Exception as e:
        print(f"❌ خطأ في قراءة ملف .env: {e}")
        return False

def test_vimeo_connection():
    """اختبار الاتصال بفيمو"""
    print("\n🔗 اختبار الاتصال بفيمو...")
    
    try:
        from dotenv import load_dotenv
        import vimeo
        
        load_dotenv()
        
        vimeo_client = vimeo.VimeoClient(
            token=os.getenv("VIMEO_ACCESS_TOKEN"),
            key=os.getenv("VIMEO_CLIENT_ID"),
            secret=os.getenv("VIMEO_CLIENT_SECRET")
        )
        
        response = vimeo_client.get("/me")
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ الاتصال بفيمو - ناجح")
            print(f"   المستخدم: {user_data.get('name', 'غير معروف')}")
            return True
        else:
            print(f"❌ خطأ في الاتصال بفيمو: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الاتصال بفيمو: {e}")
        return False

def test_telegram_bot():
    """اختبار بوت تليجرام"""
    print("\n🤖 اختبار بوت تليجرام...")
    
    try:
        from dotenv import load_dotenv
        from telegram import Bot
        
        load_dotenv()
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        
        if not bot_token or bot_token == "YOUR_BOT_TOKEN_HERE":
            print("❌ توكن البوت غير محدد")
            return False
        
        bot = Bot(token=bot_token)
        bot_info = bot.get_me()
        print(f"✅ الاتصال بالبوت - ناجح")
        print(f"   اسم البوت: {bot_info.first_name}")
        print(f"   معرف البوت: @{bot_info.username}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في الاتصال بالبوت: {e}")
        return False

def test_teacher_manager():
    """اختبار نظام إدارة المعلمين"""
    print("\n👥 اختبار نظام إدارة المعلمين...")
    
    try:
        from teacher_manager import TeacherManager
        
        manager = TeacherManager()
        
        # اختبار إضافة معلم تجريبي
        test_teacher_id = 999999999
        test_teacher_name = "معلم تجريبي للاختبار"
        
        if manager.add_teacher(test_teacher_id, test_teacher_name):
            print("✅ إضافة معلم - ناجح")
            
            # اختبار الحصول على معلومات المعلم
            teacher_info = manager.get_teacher_info(test_teacher_id)
            if teacher_info:
                print("✅ الحصول على معلومات المعلم - ناجح")
            
            # اختبار إزالة المعلم التجريبي
            if manager.remove_teacher(test_teacher_id):
                print("✅ إزالة معلم - ناجح")
            
            return True
        else:
            print("⚠️ المعلم موجود مسبقاً")
            return True
            
    except Exception as e:
        print(f"❌ خطأ في نظام إدارة المعلمين: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("🧪 اختبار نظام رفع الفيديوهات")
    print("=" * 50)
    
    tests = [
        ("استيراد المكتبات", test_imports),
        ("وجود الملفات", test_files),
        ("ملف البيئة", test_env_file),
        ("الاتصال بفيمو", test_vimeo_connection),
        ("بوت تليجرام", test_telegram_bot),
        ("نظام إدارة المعلمين", test_teacher_manager)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ خطأ في اختبار {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 نتائج الاختبار: {passed}/{total}")
    
    if passed == total:
        print("🎉 جميع الاختبارات نجحت!")
        print("✅ النظام جاهز للاستخدام")
    else:
        print("⚠️ بعض الاختبارات فشلت")
        print("💡 راجع الأخطاء أعلاه وأصلحها")
    
    print("\n💡 للتشغيل:")
    print("   python run_bot.py")

if __name__ == "__main__":
    main()