import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random

# Replace with your Bot Token
BOT_TOKEN = '7794586269:AAFkH_jflC6kpBmFUxIJOKQLCVyP0fZQqPo'

# Bible-API URL (Getting Bible verses)
BIBLE_API_URL = "https://bible-api.com/"

# Open Trivia Database API URL (Christian trivia questions)
TRIVIA_API_URL = "https://opentdb.com/api.php?amount=1&category=19&type=multiple"  # Category 19 is for Religion (Christianity)

# Fetch a Bible verse (John 3:16 as an example)
def get_bible_verse():
    response = requests.get(BIBLE_API_URL + "John 3:16")  # Example verse: John 3:16
    if response.status_code == 200:
        return response.json().get('text', 'Error: Could not fetch Bible verse')
    else:
        return "Error: Could not fetch Bible verse"

# Fetch a Christian trivia question
def get_trivia_question():
    response = requests.get(TRIVIA_API_URL)
    if response.status_code == 200:
        data = response.json()
        question = data['results'][0]['question']
        correct_answer = data['results'][0]['correct_answer']
        incorrect_answers = data['results'][0]['incorrect_answers']
        options = incorrect_answers + [correct_answer]
        random.shuffle(options)
        return question, options, correct_answer
    else:
        return "Error: Could not fetch trivia question", [], ""

# Start command
def start(update: Update, context: CallbackContext):
    user_first_name = update.message.from_user.first_name
    welcome_message = f"Hello {user_first_name}! Welcome to the Christian Bot. Ask me about the Bible, take a quiz, or learn more about Christian life!\n\nI am Stupidmoni-dev, a man who loves God but chooses to stay at home to worship Him, condemned as a pagan because I refuse to go to church. But my heart belongs to the Lord! I was born to create impact, solve problems, and make the world of tech easier for everyone!"
    
    # Send the welcome message
    update.message.reply_text(welcome_message)
    
    # Send the command list
    commands_list = (
        "Here are the commands you can use:\n"
        "/start - Start the bot and get the welcome message\n"
        "/verse - Get a Bible verse\n"
        "/quiz - Start a Christian quiz\n"
        "/answer [your answer] - Submit your answer to the quiz\n"
        "/help - Show this message"
    )
    update.message.reply_text(commands_list)

# Bible Verse command
def verse(update: Update, context: CallbackContext):
    bible_verse = get_bible_verse()
    update.message.reply_text(bible_verse)

# Quiz command
def quiz(update: Update, context: CallbackContext):
    question, options, correct_answer = get_trivia_question()
    update.message.reply_text(f"Trivia Question: {question}\nOptions: {', '.join(options)}")
    
    # Save the correct answer in the user's session (e.g., in context.user_data) for later comparison
    context.user_data['correct_answer'] = correct_answer

# Answer command for quiz
def answer(update: Update, context: CallbackContext):
    user_answer = update.message.text
    correct_answer = context.user_data.get('correct_answer')

    if user_answer.lower() == correct_answer.lower():
        update.message.reply_text("Correct! You earned 1 point.")
    else:
        update.message.reply_text(f"Incorrect. The correct answer was: {correct_answer}")

# Help command
def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Here are the commands you can use:\n"
        "/start - Start the bot\n"
        "/verse - Get a Bible verse\n"
        "/quiz - Start a Christian quiz\n"
        "/answer [your answer] - Submit your answer to the quiz\n"
        "/help - Show this message"
    )

def main():
    # Initialize the Updater
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("verse", verse))
    dp.add_handler(CommandHandler("quiz", quiz))
    dp.add_handler(CommandHandler("answer", answer))
    dp.add_handler(CommandHandler("help", help))

    # Add message handler for responding to Bible or Christian-related messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

# Handle messages
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()

    if "bible" in user_message or "christian" in user_message:
        update.message.reply_text("The Bible is God's word and it contains teachings for a righteous life. Feel free to ask about any verses or topics.")
    
    elif "love" in user_message:
        update.message.reply_text("Love is the greatest commandment. Jesus said, 'Love your neighbor as yourself.'")

    elif "god" in user_message:
        update.message.reply_text("I am a man who loves God but chooses to stay at home to worship Him, condemned as a pagan because I refuse to go to church.")

    else:
        update.message.reply_text("I am here to share knowledge about the Bible and Christian life. Ask me anything!")

if __name__ == "__main__":
    main()
