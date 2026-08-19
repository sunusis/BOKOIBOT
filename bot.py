from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

SYSTEM_PROMPT = """You are an expert professional English ↔ Hausa translator with native-level fluency in both languages.

Strict Rules:
1. Translate accurately and naturally.
2. Use correct modern Hausa grammar, spelling, and common everyday expressions.
3. Prefer natural Hausa that native speakers actually use.
4. Keep the original meaning exact.
5. Always reply in this exact format only:

🇬🇧 *English*
[English text]

🇳🇬 *Hausa*
[Hausa text]
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sannu! 👋\n\n"
        "Ni ne *BOKO Bot* – English ↔ Hausa Translator.\n\n"
        "Aika min kalma ko jumla (English ko Hausa).\n"
        "Zan fassara maka da sauri.",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
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
