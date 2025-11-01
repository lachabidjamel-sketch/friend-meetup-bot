import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import database

TOKEN = os.getenv('TELEGRAM_TOKEN')

# تهيئة قاعدة البيانات
database.init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'مرحباً! 🗓️ أنا بوت ترتيب المواعيد مع الأصدقاء\n\n'
        'استخدم /meeting لترتيب موعد جديد\n'
        'استخدم /list لرؤية مواعيدك'
    )

async def meeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🗓️ **لنرتب موعداً جديداً!**\n\n'
        'أرسل لي رسالة واحدة تحتوي على:\n'
        '👥 مع من تريد اللقاء؟\n'
        '📅 متى التاريخ والوقت؟\n'
        '📍 أين المكان؟\n\n'
        'مثال: "لقاء مع أحمد غداً الساعة 5 في المقهى"'
    )
    context.user_data['waiting_for_meeting'] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_for_meeting'):
        user_id = update.message.from_user.id
        meeting_text = update.message.text
        
        # حفظ في قاعدة البيانات
        database.add_meeting(user_id, "صديق", meeting_text, "مكان")
        
        await update.message.reply_text(
            '✅ **تم حفظ الموعد!**\n\n'
            f'تفاصيل الموعد: {meeting_text}\n\n'
            'استخدم /list لرؤية جميع مواعيدك'
        )
        context.user_data['waiting_for_meeting'] = False
    else:
        await update.message.reply_text('استخدم /meeting لترتيب موعد جديد')

async def list_meetings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    meetings = database.get_user_meetings(user_id)
    
    if not meetings:
        await update.message.reply_text('📭 لا توجد لديك مواعيد مسجلة')
        return
    
    response = '📋 **مواعيدك القادمة:**\n\n'
    for i, (friend, time, location) in enumerate(meetings, 1):
        response += f'{i}. مع {friend}\n   ⏰ {time}\n   📍 {location}\n\n'
    
    await update.message.reply_text(response)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🆘 **كيفية الاستخدام:**\n'
        '/meeting - ترتيب موعد جديد\n'
        '/list - عرض مواعيدك\n'
        '/start - رسالة الترحيب'
    )

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meeting", meeting))
    app.add_handler(CommandHandler("list", list_meetings))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ البوت يعمل مع قاعدة البيانات...")
    app.run_polling()

if __name__ == "__main__":
    main()
