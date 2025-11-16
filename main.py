import os
import json
import google.generativeai as genai
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
load_dotenv()

# Your ask_gemini function (as you provided)
def ask_gemini(question):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('data/routine_data.json', encoding='utf-8') as f:
        routine = json.load(f)
    with open('data/faculty_info.json', encoding='utf-8') as f:
        faculty = json.load(f)
    with open('data/course_info.json', encoding='utf-8') as f:
        courses = json.load(f)


    prompt = f"""
    [SYSTEM: Current date and time is {now}]
    Your name is MetroMate. You are a helpful Telegram bot for university routine, faculty, and course info. If anyone asks about your name, always reply: 'Hi, I'm MetroMate.'
    If anyone asks about your developer, reply: 'I was developed by Abu Ubayda and Nahidul Islam Roni.'
    Here is the data:
    Routine: {routine}
    Faculty: {faculty}
    Courses: {courses}
    User question: {question}
    Answer in Bangla if the question is in Bangla, otherwise in English.
    """

    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini API error: {e}"

# Telegram bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I'm MetroMate. Ask me anything about your university routine, faculty, or courses.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # Simple in-memory history (per session, not persistent)
    question = update.message.text
    answer = ask_gemini(question)
    await update.message.reply_text(answer)

def main():
    bot_token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("MetroMate bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()