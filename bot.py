from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8745652305:AAEFfbFVV2Uh9rvjkzmbo6vviO1GHxWbbDg"
ADMIN_ID = 692361687
CHANNEL_USERNAME = "@savekaroofficial"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to SaveKaro Deals Bot!\n\n"
        "Only admin can post deals.\n"
        "Use /deal to post a new offer."
    )

async def deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return

    text = update.message.text.replace("/deal", "").strip()
    if not text:
        await update.message.reply_text(
            "❌ Send deal like this:\n\n"
            "/deal\n"
            "Product: ...\n"
            "Price: ...\n"
            "Offer: ...\n"
            "Link: ..."
        )
        return

    lines = text.split("\n")
    link = ""
    for line in lines:
        if line.lower().startswith("link"):
            link = line.split(":", 1)[1].strip()

    message = "🔥 *Deal Alert!* 🔥\n\n" + "\n".join(lines)

    buttons = [
        [InlineKeyboardButton("🛒 Buy Now", url=link)],
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")]
    ]

    await context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=message,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    await update.message.reply_text("✅ Deal posted successfully!")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("deal", deal))

app.run_polling()