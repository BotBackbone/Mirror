import os
import threading
import http.server
import socketserver
from pyrogram import Client, filters, enums

# ================= CONFIG =================

api_id = int(os.environ.get("TELEGRAM_API_ID", "0"))
api_hash = os.environ.get("TELEGRAM_API_HASH", "")
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")

# TARGET CHANNEL (ID recommended)
TARGET_CHANNEL = --1003560361279  # <-- CHANGE THIS

# =========================================

app = Client(
    "pm-mirror-bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    in_memory=True
)

def fix_text(text: str | None):
    if not text:
        return None
    return text.replace("start=file_", "start=shortlink_")

@app.on_message(filters.private)
async def mirror(_, m):
    try:
        # TEXT MESSAGE
        if m.text:
            await app.send_message(
                chat_id=TARGET_CHANNEL,
                text=fix_text(m.text.html),
                parse_mode=enums.ParseMode.HTML
            )
            return

        # MEDIA / STICKERS / EVERYTHING ELSE
        caption = fix_text(m.caption.html if m.caption else None)

        await app.copy_message(
            chat_id=TARGET_CHANNEL,
            from_chat_id=m.chat.id,
            message_id=m.id,
            caption=caption,
            parse_mode=enums.ParseMode.HTML
        )

    except Exception as e:
        print(f"Mirror error: {e}")

# ================= HEALTH SERVER =================

def run_health_server():
    class HealthHandler(http.server.BaseHTTPRequestHandler):
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

# ================= START =================

if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    app.run()
