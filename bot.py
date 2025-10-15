import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json

# === Настройки ===
BOT_TOKEN = "8088096127:AAGM3rWPCASkYPP3QEik_s7RuOVqQHfb8CA"
ADMIN_CHAT_ID = 1402922835  # без кавычек

# === Логирование ===
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# === Команда /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} запустил бота.")
    keyboard = [
        [KeyboardButton("🌴 Phuket Holiday Apartments")],
        [KeyboardButton("📍 Контакты")],
        [KeyboardButton("🏡 Апартаменты")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! 👋 Мы — Александр и Ольга.\n"
        "Добро пожаловать в Phuket Holiday Apartments!\n\n"
        "Выберите действие ниже:",
        reply_markup=reply_markup
    )

# === Ответы на кнопки ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "Контакты" in text:
        await update.message.reply_text(
            "📞 Мы — Александр и Ольга.\n"
            "Связаться с нами можно:\n"
            "WhatsApp / Telegram: +66 XXX XXX XXXX\n"
            "🌐 Phuket Holiday Apartments"
        )

    elif "Апартаменты" in text:
        await update.message.reply_text(
            "🏡 У нас есть апартаменты рядом с пляжами Nai Yang и Rawai.\n"
            "Минимальный срок проживания — от 30 дней."
        )

    elif "Phuket Holiday Apartments" in text:
        await update.message.reply_text(
            "🌴 Это наш проект о жизни у моря.\n"
            "Мы делимся теплом Пхукета и сдаём собственные квартиры у моря 🏖"
        )

    else:
        await update.message.reply_text("Пожалуйста, выберите вариант из меню.")

# === Главная функция ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
