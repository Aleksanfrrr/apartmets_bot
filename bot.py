import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8088096127:AAGM3rWPCASkYPP3QEik_s7RuOVqQHfb8CA"  # <-- сюда вставь токен из BotFather

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

logger.info("BOT.PY MARKER v4 — PTB 20.8, no Updater")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [KeyboardButton("🌴 Phuket Holiday Apartments")],
        [KeyboardButton("📍 Контакты")],
        [KeyboardButton("🏡 Апартаменты")]
    ]
    await update.message.reply_text(
        "Привет! 👋 Мы — Александр и Ольга.\n"
        "Добро пожаловать в Phuket Holiday Apartments!\n\n"
        "Выберите действие ниже:",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
    )

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    if "Контакты" in text:
        await update.message.reply_text("📞 Связаться с нами можно в WhatsApp или Telegram: +66 XXX XXX XXXX")
    elif "Апартаменты" in text:
        await update.message.reply_text("🏡 Апартаменты у Nai Yang и Rawai. Минимальный срок проживания — от 30 дней.")
    elif "Phuket Holiday Apartments" in text:
        await update.message.reply_text("🌴 Наш проект о жизни у моря и уютных квартирах на Пхукете 🏖")
    else:
        await update.message.reply_text("Пожалуйста, выберите пункт из меню.")

# Основной запуск
def main():
    logger.info("Bot starting (v4)...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot started ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
