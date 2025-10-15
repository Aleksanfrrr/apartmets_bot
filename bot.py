import json, logging, os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot")

print("### MARKER: bot.py v7 — PTB ready", flush=True)

BOT_TOKEN = "8088096127:AAGM3rWPCASkYPP3QEik_s7RuOVqQHfb8CA"
ADMIN_CHAT_ID = 1402922835

LANG, PICK_APT, AFTER_APT, FORM_DATES, FORM_GUESTS, FORM_NAME, FORM_CONTACT, FORM_WISHES = range(8)
UD_LANG, UD_APT, UD_FORM = "lang", "apt_key", "form"

with open("data.json", "r", encoding="utf-8-sig") as f:
    DATA = json.load(f)

def t(lang: str, key: str) -> str:
    return DATA["texts"].get(lang, DATA["texts"]["en"]).get(key, key)

def k_lang() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("Русский", callback_data="lang:ru"),
                                   InlineKeyboardButton("English", callback_data="lang:en")]])

def k_apts(lang: str) -> InlineKeyboardMarkup:
    rows=[]
    for key, a in DATA["apartments"].items():
        title = a["ru_name"] if lang == "ru" else a["en_name"]
        rows.append([InlineKeyboardButton(title, callback_data=f"apt:{key}")])
    return InlineKeyboardMarkup(rows)

def k_yesno(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"btn_yes"), callback_data="yes"),
                                  InlineKeyboardButton(t(lang,"btn_no"),  callback_data="no")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(t("ru","choose_lang"), reply_markup=k_lang())
    return LANG

async def on_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    _, lang = q.data.split(":",1)
    context.user_data[UD_LANG]=lang

    welcome = t(lang,"welcome")
    photo = DATA.get("welcome_photo_file_id") or ""
    if photo:
        await q.message.reply_photo(photo, caption=welcome, parse_mode=ParseMode.HTML)
    else:
        await q.message.reply_text(welcome, parse_mode=ParseMode.HTML)

    await q.message.reply_text(t(lang, "which_apt"), reply_markup=k_apts(lang))
    return PICK_APT

async def on_pick_apartment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    _, apt_key = q.data.split(":",1)
    context.user_data[UD_APT]=apt_key
    lang = context.user_data.get(UD_LANG,"en")

    apt = DATA["apartments"][apt_key]
    caption = apt["ru_caption"] if lang=="ru" else apt["en_caption"]
    photo_id = apt.get("photo_file_id") or ""
    if photo_id:
        await q.message.reply_photo(photo=photo_id, caption=caption, parse_mode=ParseMode.HTML)
    else:
        await q.message.reply_text(caption, parse_mode=ParseMode.HTML)

    await q.message.reply_text(t(lang,"want_request"), reply_markup=k_yesno(lang))
    return AFTER_APT

async def on_yesno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    lang = context.user_data.get(UD_LANG,"en")
    if q.data=="no":
        await q.message.reply_text(t(lang, "which_apt"), reply_markup=k_apts(lang))
        return PICK_APT
    context.user_data[UD_FORM] = {}
    await q.message.reply_text(t(lang,"q_dates"))
    return FORM_DATES

async def form_dates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[UD_FORM]["dates"]=update.message.text.strip()
    lang=context.user_data.get(UD_LANG,"en")
    await update.message.reply_text(t(lang,"q_guests")); return FORM_GUESTS

async def form_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[UD_FORM]["guests"]=update.message.text.strip()
    lang=context.user_data.get(UD_LANG,"en")
    await update.message.reply_text(t(lang,"q_name")); return FORM_NAME

async def form_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[UD_FORM]["name"]=update.message.text.strip()
    lang=context.user_data.get(UD_LANG,"en")
    await update.message.reply_text(t(lang,"q_contact")); return FORM_CONTACT

async def form_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[UD_FORM]["contact"]=update.message.text.strip()
    lang=context.user_data.get(UD_LANG,"en")
    await update.message.reply_text(t(lang,"q_wishes")); return FORM_WISHES

async def form_wishes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data[UD_FORM]["wishes"]=update.message.text.strip()
    lang=context.user_data.get(UD_LANG,"en")
    apt_key=context.user_data.get(UD_APT)
    apt=DATA["apartments"].get(apt_key,{})
    apt_title=apt.get("ru_name") if lang=="ru" else apt.get("en_name")

    form=context.user_data.get(UD_FORM,{})
    admin_msg=( "✅ New booking request\n"
        f"Lang: {lang}\nApartment: {apt_title}\n\n"
        f"Dates: {form.get('dates','')}\nGuests: {form.get('guests','')}\n"
        f"Name: {form.get('name','')}\nContact: {form.get('contact','')}\n"
        f"Wishes: {form.get('wishes','')}\n")
    if ADMIN_CHAT_ID:
        try: await context.bot.send_message(chat_id=int(ADMIN_CHAT_ID), text=admin_msg)
        except Exception as e: logger.error(f"Admin msg error: {e}")

    await update.message.reply_text(t(lang,"request_sent"))
    await update.message.reply_text("Чтобы начать заново, нажмите /start")
    return ConversationHandler.END

async def contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang=context.user_data.get(UD_LANG,"ru")
    text_ru=("📞 <b>Контакты Phuket Holiday Apartments</b>\nСвяжитесь с нами удобным способом:")
    text_en=("📞 <b>Contacts — Phuket Holiday Apartments</b>\nReach us via your preferred method:")
    btns=[[InlineKeyboardButton("🌐 Website", url="https://phuket.holiday.apartments")],
          [InlineKeyboardButton("💬 WhatsApp", url="https://wa.me/66621839495")],
          [InlineKeyboardButton("✈️ Telegram", url="https://t.me/phuketholidayapartments")],
          [InlineKeyboardButton("📸 Instagram", url="https://instagram.com/phuket_holiday_apartments")]]
    await update.message.reply_text(text_ru if lang=="ru" else text_en,
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=InlineKeyboardMarkup(btns))

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог завершён. /start")
    return ConversationHandler.END

def build_app():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is empty")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv=ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [CallbackQueryHandler(on_lang, pattern=r"^lang:(ru|en)$")],
            PICK_APT: [CallbackQueryHandler(on_pick_apartment, pattern=r"^apt:")],
            AFTER_APT: [CallbackQueryHandler(on_yesno, pattern=r"^(yes|no)$")],
            FORM_DATES: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_dates)],
            FORM_GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_guests)],
            FORM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_name)],
            FORM_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_contact)],
            FORM_WISHES: [MessageHandler(filters.TEXT & ~filters.COMMAND, form_wishes)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("contacts", contacts))
    return app

if __name__ == "__main__":
    app = build_app()
    app.run_polling()
