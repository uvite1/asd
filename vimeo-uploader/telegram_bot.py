import os
import tempfile
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import vimeo
from dotenv import load_dotenv
from teacher_manager import TeacherManager

# تحميل المتغيرات البيئية
load_dotenv()

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# بيانات فيمو
VIMEO_ACCESS_TOKEN = os.getenv("VIMEO_ACCESS_TOKEN", "961dc516d69a070b89aeafbe1e1a104f")
VIMEO_CLIENT_ID = os.getenv("VIMEO_CLIENT_ID", "ee28d4c610482b75013cbff2a88be9576d778d96")
VIMEO_CLIENT_SECRET = os.getenv("VIMEO_CLIENT_SECRET", "xhfpAP9FNHGHyw67J347gUPCLcIuQ2FQd4/9gnbSXB0ZUQ/R2lili6UUt/3TTA23j9CALTcTP/PIQ2jEKbkbGXvdbwIERat04VDNF6LAVtSUEaRwdk4b6Va0qO+BTq1c")

# توكن بوت تليجرام - يجب تغييره
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# إنشاء عميل فيمو
vimeo_client = vimeo.VimeoClient(
    token=VIMEO_ACCESS_TOKEN,
    key=VIMEO_CLIENT_ID,
    secret=VIMEO_CLIENT_SECRET
)

# إنشاء مدير المعلمين
teacher_manager = TeacherManager()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """رسالة الترحيب عند بدء البوت"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # التحقق من صلاحية المستخدم
    if not teacher_manager.is_authorized(user_id):
        welcome_message = f"""
مرحباً {user_name}! 👋

أنا بوت رفع الفيديوهات إلى فيمو 📹

❌ عذراً، أنت غير مصرح لك باستخدام هذا البوت حالياً.

📞 للطلب:
راسل المدير لإضافة اسمك إلى قائمة المعلمين المصرح لهم.
"""
    else:
        welcome_message = f"""
مرحباً {user_name}! 👋

أنا بوت رفع الفيديوهات إلى فيمو 📹

📋 كيفية الاستخدام:
• أرسل لي أي فيديو تريد رفعه إلى فيمو
• سأقوم برفعه تلقائياً وإرسال الرابط لك

📊 إحصائياتك:
• عدد الفيديوهات المرفوعة: {teacher_manager.get_teacher_info(user_id).get('upload_count', 0)}

📋 الأوامر المتاحة:
/help - عرض المساعدة
/status - حالة البوت
/stats - إحصائياتك
"""
    
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """رسالة المساعدة"""
    user_id = update.effective_user.id
    
    if not teacher_manager.is_authorized(user_id):
        await update.message.reply_text("❌ عذراً، أنت غير مصرح لك باستخدام هذا البوت.")
        return
    
    help_text = """
📚 دليل الاستخدام:

🎥 لرفع فيديو:
• أرسل الفيديو مباشرة للبوت
• أو أرسل ملف فيديو كملف

📋 الأوامر المتاحة:
/start - بدء البوت
/help - عرض هذه الرسالة
/status - حالة البوت
/stats - إحصائياتك

📞 للدعم الفني:
راسل المدير في حالة وجود مشاكل

⚠️ ملاحظات:
• الحد الأقصى لحجم الفيديو: 50 ميجابايت
• صيغ الفيديو المدعومة: MP4, AVI, MOV, MKV
"""
    
    await update.message.reply_text(help_text)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """عرض إحصائيات المعلم"""
    user_id = update.effective_user.id
    
    if not teacher_manager.is_authorized(user_id):
        await update.message.reply_text("❌ عذراً، أنت غير مصرح لك باستخدام هذا البوت.")
        return
    
    teacher_info = teacher_manager.get_teacher_info(user_id)
    if teacher_info:
        stats_message = f"""
📊 إحصائياتك:

👤 الاسم: {teacher_info['name']}
🎭 الدور: {teacher_info['role']}
📅 تاريخ التسجيل: {teacher_info['created_at'][:10]}
📹 عدد الفيديوهات المرفوعة: {teacher_info['upload_count']}
✅ الحالة: {'نشط' if teacher_info['active'] else 'غير نشط'}
"""
    else:
        stats_message = "❌ لم يتم العثور على معلوماتك"
    
    await update.message.reply_text(stats_message)

async def admin_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """عرض إحصائيات عامة (للمديرين فقط)"""
    user_id = update.effective_user.id
    
    if not teacher_manager.is_authorized(user_id):
        await update.message.reply_text("❌ عذراً، أنت غير مصرح لك باستخدام هذا البوت.")
        return
    
    teacher_info = teacher_manager.get_teacher_info(user_id)
    if teacher_info and teacher_info.get('role') == 'admin':
        stats = teacher_manager.get_statistics()
        admin_message = f"""
📊 إحصائيات النظام:

👥 إجمالي المعلمين: {stats['total_teachers']}
✅ المعلمين النشطين: {stats['active_teachers']}
📹 إجمالي الفيديوهات المرفوعة: {stats['total_uploads']}
📈 متوسط الرفعات لكل معلم: {stats['average_uploads']:.1f}

🔧 أوامر الإدارة:
/add_teacher [user_id] [name] - إضافة معلم
/remove_teacher [user_id] - إزالة معلم
/toggle_teacher [user_id] - تفعيل/إلغاء تفعيل معلم
"""
    else:
        admin_message = "❌ عذراً، هذا الأمر متاح للمديرين فقط"
    
    await update.message.reply_text(admin_message)

async def add_teacher_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إضافة معلم جديد (للمديرين فقط)"""
    user_id = update.effective_user.id
    
    if not teacher_manager.is_authorized(user_id):
        await update.message.reply_text("❌ عذراً، أنت غير مصرح لك باستخدام هذا البوت.")
        return
    
    teacher_info = teacher_manager.get_teacher_info(user_id)
    if not teacher_info or teacher_info.get('role') != 'admin':
        await update.message.reply_text("❌ عذراً، هذا الأمر متاح للمديرين فقط")
        return
    
    # التحقق من وجود المعاملات المطلوبة
    if len(context.args) < 2:
        await update.message.reply_text("❌ الاستخدام الصحيح: /add_teacher [user_id] [name]")
        return
    
    try:
        new_user_id = int(context.args[0])
        new_teacher_name = " ".join(context.args[1:])
        
        if teacher_manager.add_teacher(new_user_id, new_teacher_name):
            await update.message.reply_text(f"✅ تم إضافة المعلم {new_teacher_name} بنجاح")
        else:
            await update.message.reply_text("❌ المعلم موجود مسبقاً")
    except ValueError:
        await update.message.reply_text("❌ معرف المستخدم غير صحيح")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالجة الفيديوهات المرسلة"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # التحقق من صلاحية المستخدم
    if not teacher_manager.is_authorized(user_id):
        await update.message.reply_text("❌ عذراً، أنت غير مصرح لك باستخدام هذا البوت.")
        return
    
    # إرسال رسالة "جاري المعالجة"
    processing_msg = await update.message.reply_text("⏳ جاري معالجة الفيديو...")
    
    try:
        # الحصول على معلومات الفيديو
        video = update.message.video
        if not video:
            await processing_msg.edit_text("❌ لم يتم العثور على فيديو في الرسالة")
            return
        
        # التحقق من حجم الفيديو (50 ميجابايت كحد أقصى)
        if video.file_size > 50 * 1024 * 1024:
            await processing_msg.edit_text("❌ حجم الفيديو كبير جداً. الحد الأقصى 50 ميجابايت")
            return
        
        # تحميل الفيديو
        file = await context.bot.get_file(video.file_id)
        
        # حفظ الفيديو في ملف مؤقت
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            await file.download_to_drive(tmp_file.name)
            tmp_path = tmp_file.name
        
        # رفع الفيديو إلى فيمو
        await processing_msg.edit_text("📤 جاري رفع الفيديو إلى فيمو...")
        
        # استخدام اسم الملف كعنوان إذا لم يكن هناك عنوان
        title = video.file_name or f"فيديو من {user_name}"
        
        # رفع الفيديو
        uri = vimeo_client.upload(tmp_path, data={"name": title})
        video_id = uri.rsplit("/", 1)[1]
        vimeo_url = f"https://vimeo.com/{video_id}"
        
        # زيادة عداد الرفعات للمعلم
        teacher_manager.increment_upload_count(user_id)
        
        # إنشاء أزرار للتفاعل
        keyboard = [
            [InlineKeyboardButton("🔗 رابط فيمو", url=vimeo_url)],
            [InlineKeyboardButton("📱 مشاركة", switch_inline_query=vimeo_url)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # رسالة النجاح
        success_message = f"""
✅ تم رفع الفيديو بنجاح!

📹 العنوان: {title}
👤 المعلم: {user_name}
🔗 الرابط: {vimeo_url}

📊 معلومات الفيديو:
• الحجم: {video.file_size / (1024*1024):.1f} MB
• المدة: {video.duration} ثانية

📈 إجمالي رفعاتك: {teacher_manager.get_teacher_info(user_id).get('upload_count', 0)}
"""
        
        await processing_msg.edit_text(success_message, reply_markup=reply_markup)
        
        # إرسال رسالة منفصلة بالرابط
        await update.message.reply_text(
            f"🎉 تم رفع الفيديو بنجاح!\n🔗 {vimeo_url}",
            reply_markup=reply_markup
        )
        
    except Exception as e:
        error_message = f"❌ حدث خطأ أثناء رفع الفيديو:\n{str(e)}"
        await processing_msg.edit_text(error_message)
        logger.error(f"Error uploading video: {e}")
    
    finally:
        # حذف الملف المؤقت
        if 'tmp_path' in locals():
            try:
                os.remove(tmp_path)
            except:
                pass

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالجة الملفات المرسلة (مثل الفيديوهات كملفات)"""
    user_id = update.effective_user.id
    
    # التحقق من صلاحية المستخدم
    if not teacher_manager.is_authorized(user_id):
        await update.message.reply_text("❌ عذراً، أنت غير مصرح لك باستخدام هذا البوت.")
        return
    
    document = update.message.document
    
    # التحقق من أن الملف هو فيديو
    if not document.mime_type or not document.mime_type.startswith('video/'):
        await update.message.reply_text("❌ يرجى إرسال ملف فيديو صالح")
        return
    
    # التحقق من حجم الملف
    if document.file_size > 50 * 1024 * 1024:
        await update.message.reply_text("❌ حجم الملف كبير جداً. الحد الأقصى 50 ميجابايت")
        return
    
    # إرسال رسالة "جاري المعالجة"
    processing_msg = await update.message.reply_text("⏳ جاري معالجة ملف الفيديو...")
    
    try:
        # تحميل الملف
        file = await context.bot.get_file(document.file_id)
        
        # حفظ الملف في ملف مؤقت
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            await file.download_to_drive(tmp_file.name)
            tmp_path = tmp_file.name
        
        # رفع الفيديو إلى فيمو
        await processing_msg.edit_text("📤 جاري رفع الفيديو إلى فيمو...")
        
        # استخدام اسم الملف كعنوان
        title = document.file_name or "فيديو"
        
        # رفع الفيديو
        uri = vimeo_client.upload(tmp_path, data={"name": title})
        video_id = uri.rsplit("/", 1)[1]
        vimeo_url = f"https://vimeo.com/{video_id}"
        
        # زيادة عداد الرفعات للمعلم
        teacher_manager.increment_upload_count(user_id)
        
        # إنشاء أزرار للتفاعل
        keyboard = [
            [InlineKeyboardButton("🔗 رابط فيمو", url=vimeo_url)],
            [InlineKeyboardButton("📱 مشاركة", switch_inline_query=vimeo_url)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # رسالة النجاح
        success_message = f"""
✅ تم رفع الفيديو بنجاح!

📹 العنوان: {title}
🔗 الرابط: {vimeo_url}

📊 معلومات الملف:
• الحجم: {document.file_size / (1024*1024):.1f} MB

📈 إجمالي رفعاتك: {teacher_manager.get_teacher_info(user_id).get('upload_count', 0)}
"""
        
        await processing_msg.edit_text(success_message, reply_markup=reply_markup)
        
        # إرسال رسالة منفصلة بالرابط
        await update.message.reply_text(
            f"🎉 تم رفع الفيديو بنجاح!\n🔗 {vimeo_url}",
            reply_markup=reply_markup
        )
        
    except Exception as e:
        error_message = f"❌ حدث خطأ أثناء رفع الفيديو:\n{str(e)}"
        await processing_msg.edit_text(error_message)
        logger.error(f"Error uploading document: {e}")
    
    finally:
        # حذف الملف المؤقت
        if 'tmp_path' in locals():
            try:
                os.remove(tmp_path)
            except:
                pass

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """عرض حالة البوت"""
    user_id = update.effective_user.id
    
    if not teacher_manager.is_authorized(user_id):
        await update.message.reply_text("❌ عذراً، أنت غير مصرح لك باستخدام هذا البوت.")
        return
    
    stats = teacher_manager.get_statistics()
    status_message = f"""
📊 حالة البوت:

✅ البوت يعمل بشكل طبيعي
🔗 متصل بـ Vimeo API
👤 معرف المستخدم: {user_id}

📈 إحصائيات النظام:
• إجمالي المعلمين: {stats['total_teachers']}
• المعلمين النشطين: {stats['active_teachers']}
• إجمالي الفيديوهات المرفوعة: {stats['total_uploads']}
"""
    
    await update.message.reply_text(status_message)

def main() -> None:
    """تشغيل البوت"""
    # إنشاء التطبيق
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("admin_stats", admin_stats_command))
    application.add_handler(CommandHandler("add_teacher", add_teacher_command))
    
    # معالجة الفيديوهات والملفات
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))
    application.add_handler(MessageHandler(filters.Document.VIDEO, handle_document))
    
    # تشغيل البوت
    print("🤖 بدء تشغيل بوت رفع الفيديوهات...")
    print("📝 تأكد من تعيين TELEGRAM_BOT_TOKEN في ملف .env")
    print("👥 عدد المعلمين المصرح لهم:", len(teacher_manager.get_active_teachers()))
    application.run_polling()

if __name__ == '__main__':
    main()