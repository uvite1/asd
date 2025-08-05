import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from tusclient import client as tus_client
from threading import Thread

# Load secrets from environment variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
VIMEO_TOKEN = os.environ.get("VIMEO_TOKEN")

if not TELEGRAM_TOKEN or not VIMEO_TOKEN:
    raise Exception("TELEGRAM_TOKEN and VIMEO_TOKEN must be set as environment variables.")

def upload_to_vimeo(file_path):
    """Uploads a video file to Vimeo using the TUS protocol and returns the video ID."""
    video_name = os.path.basename(file_path)
    size = os.path.getsize(file_path)

    # Step 1: Create Vimeo upload link
    headers = {
        "Authorization": f"bearer {VIMEO_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.vimeo.*+json;version=3.4",
    }

    response = requests.post(
        "https://api.vimeo.com/me/videos",
        headers=headers,
        json={
            "upload": {"approach": "tus", "size": size},
            "name": video_name
        }
    )

    if response.status_code >= 300:
        raise Exception(f"Create upload link failed: {response.status_code} - {response.text}")

    upload_info = response.json()
    upload_link = upload_info["upload"]["upload_link"]
    video_uri = upload_info["uri"]
    video_id = video_uri.split("/")[-1]

    # Step 2: Upload the file using TUS
    tus = tus_client.TusClient(upload_link, headers={"Authorization": f"bearer {VIMEO_TOKEN}"})
    uploader = tus.uploader(file_path=file_path, chunk_size=5242880, url=upload_link)

    while not uploader.finished:
        uploader.upload_chunk()

    return video_id

def handle_upload_async(file_path, chat_id, bot):
    """Handles the Vimeo upload in a separate thread and notifies the user."""
    try:
        video_id = upload_to_vimeo(file_path)
        link = f"https://vimeo.com/{video_id}"
        bot.send_message(chat_id=chat_id, text=f"✅ Video uploaded successfully!\n🔗 {link}\n🆔 {video_id}")
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"❌ Upload failed:\n{e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming video or video document messages."""
    video = update.message.video or update.message.document
    if not video:
        await update.message.reply_text("❌ Please send a valid video.")
        return

    file = await context.bot.get_file(video.file_id)
    file_path = f"video_{video.file_id}.mp4"
    chat_id = update.message.chat_id

    try:
        await update.message.reply_text("📥 Downloading video...")
        await file.download_to_drive(file_path)
        await update.message.reply_text("🚀 Uploading to Vimeo, please wait...")
        Thread(target=handle_upload_async, args=(file_path, chat_id, context.bot)).start()
    except Exception as e:
        await update.message.reply_text(f"❌ Download failed: {e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()