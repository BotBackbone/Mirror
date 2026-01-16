import os
from pyrogram import Client, filters, enums

api_id = int(os.environ.get("TELEGRAM_API_ID", "0"))
api_hash = os.environ.get("TELEGRAM_API_HASH", "")
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")

app = Client(
    "pm-mirror-bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    in_memory=True
)

@app.on_message(filters.private)
async def mirror(_, m):
    text = m.text.html if m.text else None
    caption = m.caption.html if m.caption else None

    if m.text:
        text = m.text.html if m.text else None
        if text:
            text = text.replace("start=file_", "start=shortlink_")
        await m.reply(text, parse_mode=enums.ParseMode.HTML)

    elif m.document:
        caption = m.caption.html if m.caption else None
        if caption:
            caption = caption.replace("start=file_", "start=shortlink_")
        await m.reply_document(
            m.document.file_id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

    elif m.photo:
        caption = m.caption.html if m.caption else None
        if caption:
            caption = caption.replace("start=file_", "start=shortlink_")
        await m.reply_photo(
            m.photo.file_id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

    elif m.video:
        caption = m.caption.html if m.caption else None
        if caption:
            caption = caption.replace("start=file_", "start=shortlink_")
        await m.reply_video(
            m.video.file_id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

    elif m.audio:
        caption = m.caption.html if m.caption else None
        if caption:
            caption = caption.replace("start=file_", "start=shortlink_")
        await m.reply_audio(
            m.audio.file_id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

    elif m.voice:
        caption = m.caption.html if m.caption else None
        if caption:
            caption = caption.replace("start=file_", "start=shortlink_")
        await m.reply_voice(
            m.voice.file_id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

    elif m.sticker:
        await m.reply_sticker(m.sticker.file_id)

    elif m.animation:
        caption = m.caption.html if m.caption else None
        if caption:
            caption = caption.replace("start=file_", "start=shortlink_")
        await m.reply_animation(
            m.animation.file_id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

import threading
import http.server
import socketserver

def run_health_server():
    class HealthHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Bot is running")

        def log_message(self, format, *args):
            return

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", 8080), HealthHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    app.run()
