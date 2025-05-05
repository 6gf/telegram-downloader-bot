import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp

TOKEN = "توكن البوت حقك هنا"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل رابط من YouTube أو TikTok أو Twitter لتحميله.")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("جارٍ التحميل...")

    try:
        ydl_opts = {
            'outtmpl': 'downloaded.%(ext)s',
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await update.message.reply_video(video=open(file_path, 'rb'))

    except Exception as e:
        await update.message.reply_text(f"صار خطأ: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", start))
app.add_handler(CommandHandler("dl", download))

print("Bot running...")
app.run_polling()
