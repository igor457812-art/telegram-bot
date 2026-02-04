import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import anthropic

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = "sk-ant-api03-uUYP5GfyrSaonqMfMJPeDQR-mw1hfoWz1k5qUr0ERIXW9_YNZspOAfb7aJO_IMkX2vLGcstAATPkAMa-vFHkKg-YsK_ZQAA"
AI_MODEL = os.getenv("AI_MODEL", "claude-3-5-sonnet-latest")
print("ENV CHECK: TELEGRAM_TOKEN set =", bool(TELEGRAM_TOKEN))
print("ENV CHECK: ANTHROPIC_API_KEY set =", bool(ANTHROPIC_API_KEY))
if ANTHROPIC_API_KEY:
    print("ENV CHECK: ANTHROPIC_API_KEY prefix =", ANTHROPIC_API_KEY[:7])

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.messages.create(
        model=AI_MODEL,
        max_tokens=500,
        messages=[
            {"role": "user", "content": user_text}
        ]
    )

    await update.message.reply_text(response.content[0].text)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
