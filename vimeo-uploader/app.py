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