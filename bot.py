from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://agentrouter.org/v1"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

user_usage = {}
FREE_LIMIT = 7

SYSTEM_PROMPT = """You are a professional English to Hausa translator.
If the user writes in English, translate to Hausa.
If the user writes in Hausa, translate to English.
Reply in this format:

English: [original]
Hausa: [translation]
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sannu! 👋\n\nNi ne English ↔ Hausa Translator Bot.\nAika min kalma ko jumla."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    usage = user_usage.get(user_id, 0)
    if usage >= FREE_LIMIT:
        await update.message.reply_text("Ka gama kyauta ta yau.")
        return

    try:
        response = client.chat.completions.create(
            model="gpt-5.5",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ]
        )
        result = response.choices[0].message.content
    except Exception as e:
        result = f"Error: {str(e)}"

    user_usage[user_id] = usage + 1
    await update.message.reply_text(result)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
