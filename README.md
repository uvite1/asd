# Vimeo Uploader - رفع الفيديوهات إلى Vimeo

مشروع بسيط مبني على Flask لرفع الفيديوهات إلى منصة Vimeo.

## 📦 تحميل المشروع

[تحميل الملف](./upload_script.zip.zip)

## 🚀 كيفية الاستخدام

### 1. تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### 2. إعداد بيانات الاعتماد

قم بتعديل البيانات التالية في ملف `app.py`:

```python
VIMEO_ACCESS_TOKEN  = "your_access_token_here"
VIMEO_CLIENT_ID     = "your_client_id_here"
VIMEO_CLIENT_SECRET = "your_client_secret_here"
```

### 3. تشغيل التطبيق

```bash
python app.py
```

ثم افتح المتصفح على: `http://localhost:5000`

## 📋 المتطلبات

```
flask>=2.0.0
PyVimeo>=1.1.2
python-dotenv>=0.19.0
```

## 💻 الكود الرئيسي

### app.py

```python
"""
Very small Flask-based Vimeo uploader.
Replace the three XXX… constants with your own credentials or
set the same names in the environment before you run the app.
"""

import os
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash
import vimeo   # pip install PyVimeo flask python-dotenv (optional)

# ── credentials (global) ────────────────────────────────────────────────────────
VIMEO_ACCESS_TOKEN  = os.getenv("VIMEO_ACCESS_TOKEN",  "961dc516d69a070b89aeafbe1e1a104f")
VIMEO_CLIENT_ID     = os.getenv("VIMEO_CLIENT_ID",     "ee28d4c610482b75013cbff2a88be9576d778d96")
VIMEO_CLIENT_SECRET = os.getenv("VIMEO_CLIENT_SECRET", "xhfpAP9FNHGHyw67J347gUPCLcIuQ2FQd4/9gnbSXB0ZUQ/R2lili6UUt/3TTA23j9CALTcTP/PIQ2jEKbkbGXvdbwIERat04VDNF6LAVtSUEaRwdk4b6Va0qO+BTq1c")

v = vimeo.VimeoClient(
        token=VIMEO_ACCESS_TOKEN,
        key=VIMEO_CLIENT_ID,
        secret=VIMEO_CLIENT_SECRET
)  # raises if any token is wrong

# ── Flask setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "change-me-in-prod"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    # grab form data
    f     = request.files.get("video")
    title = request.form.get("title") or (f.filename if f else "")
    if not f:
        flash("No file selected"); return redirect(url_for("index"))

    # save to a tmp file (Vimeo SDK wants a path)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        f.save(tmp)
        tmp_path = tmp.name

    try:
        # single call does *all* the resumable gymnastics for you
        uri = v.upload(tmp_path, data={"name": title})  # ← key line
        video_id = uri.rsplit("/", 1)[1]
        flash(f"✅ Uploaded — watch at https://vimeo.com/{video_id}")
    except Exception as err:
        flash(f"❌ Upload failed: {err}")
    finally:
        os.remove(tmp_path)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)          # python app.py
```

## 🔧 الميزات

- ✅ واجهة ويب بسيطة لرفع الفيديوهات
- ✅ دعم استئناف الرفع التلقائي
- ✅ رسائل تأكيد نجاح/فشل العملية
- ✅ رابط مباشر للفيديو بعد الرفع

## ⚠️ ملاحظات مهمة

1. تأكد من تحديث بيانات الاعتماد الخاصة بك
2. غير `app.secret_key` في بيئة الإنتاج
3. تأكد من أن لديك صلاحيات رفع على حساب Vimeo

## 📝 الترخيص

هذا المشروع مفتوح المصدر ومتاح للاستخدام الشخصي والتجاري.
