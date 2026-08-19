from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Store user mode and last answer
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"mode": None, "last_answer": None}

    text = (
        "Sannu! 👋\n\n"
        "Ni ne *BOKO Bot*\n\n"
        "Please choose an option:\n\n"
        "1️⃣ English ↔ Hausa Translation\n"
        "2️⃣ Science Subjects\n"
        "3️⃣ Art Subjects\n"
        "4️⃣ Cryptocurrency\n\n"
        "Just type the number (1, 2, 3 or 4)"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in user_data:
        user_data[user_id] = {"mode": None, "last_answer": None}

    # Menu selection
    if text in ["1", "2", "3", "4"]:
        if text == "1":
            user_data[user_id]["mode"] = "translation"
            await update.message.reply_text(
                "✅ *Translation Mode Activated*\n\n"
                "Aika min kalma ko jumla (English ko Hausa).",
                parse_mode="Markdown"
            )
        elif text == "2":
            user_data[user_id]["mode"] = "science"
            await update.message.reply_text(
                "📚 *Science Subjects*\n\n"
                "You can ask questions from:\n"
                "• Biology\n• Chemistry\n• Physics\n• Mathematics\n"
                "• Agricultural Science\n• Geography\n• Computer Science\n\n"
                "Just type your question.",
                parse_mode="Markdown"
            )
        elif text == "3":
            user_data[user_id]["mode"] = "art"
            await update.message.reply_text(
                "🎨 *Art Subjects*\n\n"
                "You can ask questions from:\n"
                "• Literature\n• History\n• Government\n• Economics\n"
                "• Civic Education\n• Islamic Studies\n• Christian Religious Studies\n• Fine Art\n\n"
                "Just type your question.",
                parse_mode="Markdown"
            )
        elif text == "4":
            user_data[user_id]["mode"] = "crypto"
            await update.message.reply_text(
                "💰 *Cryptocurrency Mode*\n\n"
                "You can ask about Bitcoin, Blockchain, Trading, Wallets, etc.\n\n"
                "Just type your question.",
                parse_mode="Markdown"
            )
        return

    # If user wants Hausa translation of last answer
    if text.lower() == "hausa" and user_data[user_id].get("last_answer"):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Translate the following English text to Hausa. Only return the Hausa translation."},
                    {"role": "user", "content": user_data[user_id]["last_answer"]}
                ],
                temperature=0.3
            )
            hausa = response.choices[0].message.content
            await update.message.reply_text(f"🇳🇬 *Hausa Translation:*\n\n{hausa}", parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        return

    mode = user_data[user_id].get("mode")

    if not mode:
        await update.message.reply_text("Please type /start and choose an option first (1, 2, 3 or 4).")
        return

    # Translation Mode
    if mode == "translation":
        system_prompt = """You are a professional English ↔ Hausa translator.
Reply in this exact format:

🇬🇧 *English*
[English text]

🇳🇬 *Hausa*
[Hausa text]
"""
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.3
            )
            result = response.choices[0].message.content
            await update.message.reply_text(result, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        return

    # Science / Art / Crypto Mode
    subject_type = {
        "science": "Science (Biology, Chemistry, Physics, Mathematics, Agricultural Science, Geography, Computer Science)",
        "art": "Art (Literature, History, Government, Economics, Civic Education, Islamic Studies, Christian Religious Studies, Fine Art)",
        "crypto": "Cryptocurrency (Bitcoin, Blockchain, Trading, Wallets, Crypto basics)"
    }

    system_prompt = f"""You are a helpful teacher specializing in {subject_type[mode]}.
Give a clear and brief answer in English only.
Keep the answer short and easy to understand.
Do not translate to Hausa.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.4
        )
        answer = response.choices[0].message.content
        user_data[user_id]["last_answer"] = answer

        final_reply = f"{answer}\n\nReply *Hausa* if you want this answer in Hausa."
        await update.message.reply_text(final_reply, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()        "Zan fassara maka da sauri.",
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
