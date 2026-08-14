from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

SYSTEM_PROMPT = """You are a professional English ↔ Hausa translator.

Rules:
- If the user writes in English, translate it to Hausa.
- If the user writes in Hausa, translate it to English.
- Always reply in this exact format only (use Markdown):

🇬🇧 *English*
[English text]

🇳🇬 *Hausa*
[Hausa text]

Do not add any extra text or explanation.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sannu! 👋\n\n"
        "Ni ne *English ↔ Hausa Translator Bot*.\n\n"
        "Aika min kalma ko jumla (English ko Hausa).\n"
        "Zan fassara maka da sauri.",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        result = response.choices[0].message.content
    except Exception as e:
        result = f"❌ Error: {str(e)}"

    await update.message.reply_text(result, parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
