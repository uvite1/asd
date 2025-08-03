#!/usr/bin/env python3
"""
سكريبت إعداد نظام رفع الفيديوهات من تليجرام إلى فيمو
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """طباعة شعار النظام"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    نظام رفع الفيديوهات                        ║
║                من تليجرام إلى فيمو 📹🤖                      ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_python_version():
    """التحقق من إصدار Python"""
    print("🔍 التحقق من إصدار Python...")
    if sys.version_info < (3, 8):
        print("❌ يتطلب النظام Python 3.8 أو أحدث")
        print(f"   الإصدار الحالي: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - مناسب")
    return True

def install_requirements():
    """تثبيت المتطلبات"""
    print("\n📦 تثبيت المتطلبات...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ تم تثبيت المتطلبات بنجاح")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ خطأ في تثبيت المتطلبات: {e}")
        return False

def create_env_file():
    """إنشاء ملف البيئة"""
    print("\n⚙️ إعداد ملف البيئة...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("⚠️ ملف .env موجود مسبقاً")
        overwrite = input("هل تريد استبداله؟ (y/n): ").lower()
        if overwrite != 'y':
            print("✅ تم الاحتفاظ بالملف الحالي")
            return True
    
    print("\n📝 يرجى إدخال البيانات المطلوبة:")
    
    # بيانات فيمو
    print("\n🔗 بيانات فيمو:")
    vimeo_token = input("Access Token: ").strip()
    vimeo_client_id = input("Client ID: ").strip()
    vimeo_client_secret = input("Client Secret: ").strip()
    
    # توكن البوت
    print("\n🤖 بيانات بوت تليجرام:")
    bot_token = input("Bot Token: ").strip()
    
    # إنشاء ملف .env
    env_content = f"""# بيانات فيمو
VIMEO_ACCESS_TOKEN={vimeo_token}
VIMEO_CLIENT_ID={vimeo_client_id}
VIMEO_CLIENT_SECRET={vimeo_client_secret}

# توكن بوت تليجرام
TELEGRAM_BOT_TOKEN={bot_token}

# قائمة المعلمين المصرح لهم (اختياري)
# AUTHORIZED_TEACHERS=123456789,987654321
"""
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ تم إنشاء ملف .env بنجاح")
        return True
    except Exception as e:
        print(f"❌ خطأ في إنشاء ملف .env: {e}")
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
        
        # اختبار الاتصال
        response = vimeo_client.get("/me")
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ تم الاتصال بنجاح")
            print(f"   المستخدم: {user_data.get('name', 'غير معروف')}")
            return True
        else:
            print(f"❌ خطأ في الاتصال: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار الاتصال: {e}")
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
        print(f"✅ تم الاتصال بالبوت بنجاح")
        print(f"   اسم البوت: {bot_info.first_name}")
        print(f"   معرف البوت: @{bot_info.username}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار البوت: {e}")
        return False

def create_sample_teacher():
    """إنشاء معلم تجريبي"""
    print("\n👥 إنشاء معلم تجريبي...")
    try:
        from teacher_manager import TeacherManager
        
        manager = TeacherManager()
        
        # إضافة معلم تجريبي
        sample_teacher_id = 123456789  # يمكن تغييره
        sample_teacher_name = "معلم تجريبي"
        
        if manager.add_teacher(sample_teacher_id, sample_teacher_name, "admin"):
            print(f"✅ تم إنشاء معلم تجريبي")
            print(f"   معرف المستخدم: {sample_teacher_id}")
            print(f"   الاسم: {sample_teacher_name}")
            print(f"   الدور: مدير")
            print("\n⚠️ تذكر تغيير معرف المستخدم لمعرفك الحقيقي!")
            return True
        else:
            print("⚠️ المعلم التجريبي موجود مسبقاً")
            return True
            
    except Exception as e:
        print(f"❌ خطأ في إنشاء المعلم التجريبي: {e}")
        return False

def show_next_steps():
    """عرض الخطوات التالية"""
    print("\n" + "="*60)
    print("🎉 تم إعداد النظام بنجاح!")
    print("="*60)
    
    print("\n📋 الخطوات التالية:")
    print("1. 🔧 تعديل معرف المستخدم في ملف teachers.json")
    print("2. 🚀 تشغيل البوت: python telegram_bot.py")
    print("3. 📱 اختبار البوت في تليجرام")
    print("4. 👥 إضافة المعلمين الآخرين")
    
    print("\n📚 للمزيد من المعلومات:")
    print("   - راجع README_TELEGRAM.md")
    print("   - تحقق من ملف .env")
    print("   - راقب سجلات البوت")
    
    print("\n🔧 أوامر مفيدة:")
    print("   python telegram_bot.py          # تشغيل البوت")
    print("   python teacher_manager.py       # إدارة المعلمين")
    print("   python app.py                   # التطبيق القديم")

def main():
    """الدالة الرئيسية"""
    print_banner()
    
    # التحقق من Python
    if not check_python_version():
        return
    
    # تثبيت المتطلبات
    if not install_requirements():
        return
    
    # إنشاء ملف البيئة
    if not create_env_file():
        return
    
    # اختبار الاتصالات
    if not test_vimeo_connection():
        print("⚠️ تحقق من بيانات فيمو في ملف .env")
    
    if not test_telegram_bot():
        print("⚠️ تحقق من توكن البوت في ملف .env")
    
    # إنشاء معلم تجريبي
    create_sample_teacher()
    
    # عرض الخطوات التالية
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ تم إلغاء العملية")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        print("يرجى مراجعة الأخطاء أعلاه وإعادة المحاولة")