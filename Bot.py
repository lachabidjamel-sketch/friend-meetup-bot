```
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('مرحباً! 🗓️ أنا بوت ترتيب المواعيد مع الأصدقاء\n\nاستخدم /meeting لترتيب موعد جديد')

async def meeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🗓️ **لنرتب موعداً جديداً!**\n\nأرسل لي:\n👥 مع من تريد اللقاء؟\n📅 متى التاريخ والوقت؟\n📍 أين المكان؟')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🆘 **كيفية الاستخدام:**\n/meeting - ترتيب موعد جديد\n/start - رسالة الترحيب')

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meeting", meeting))
    app.add_handler(CommandHandler("help", help_command))
    
    print("البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
```
