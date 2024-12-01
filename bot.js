const TelegramBot = require('node-telegram-bot-api');

// Replace with your bot token
const BOT_TOKEN = '7794586269:AAFkH_jflC6kpBmFUxIJOKQLCVyP0fZQqPo';

// Create a bot instance
const bot = new TelegramBot(BOT_TOKEN, { polling: true });

// Handle /start command
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    const firstName = msg.from.first_name;
    const welcomeMessage = `Hello ${firstName}! Welcome to the Christian Bot. Ask me about the Bible, take a quiz, or learn more about Christian life!`;
    bot.sendMessage(chatId, welcomeMessage);
});

// Handle /verse command to get a Bible verse
bot.onText(/\/verse/, (msg) => {
    const chatId = msg.chat.id;
    const bibleVerse = "John 3:16 - For God so loved the world that He gave His one and only Son, that whoever believes in Him shall not perish but have eternal life.";
    bot.sendMessage(chatId, bibleVerse);
});

// Handle /quiz command to start a trivia question
bot.onText(/\/quiz/, async (msg) => {
    const chatId = msg.chat.id;
    const triviaQuestion = "Who was the first king of Israel?";
    const options = ['Saul', 'David', 'Solomon', 'Samuel'];
    bot.sendMessage(chatId, triviaQuestion, {
        reply_markup: {
            inline_keyboard: [
                options.map(option => ({
                    text: option,
                    callback_data: option
                }))
            ]
        }
    });
});

// Handle quiz answers
bot.on('callback_query', (callbackQuery) => {
    const chatId = callbackQuery.message.chat.id;
    const selectedAnswer = callbackQuery.data;
    const correctAnswer = 'Saul';

    if (selectedAnswer === correctAnswer) {
        bot.sendMessage(chatId, 'Correct! You earned 1 point.');
    } else {
        bot.sendMessage(chatId, `Incorrect. The correct answer was: ${correctAnswer}`);
    }
});

// Handle /help command
bot.onText(/\/help/, (msg) => {
    const chatId = msg.chat.id;
    const helpMessage = `Here are the commands you can use:\n/start - Start the bot\n/verse - Get a Bible verse\n/quiz - Start a Christian quiz\n/answer [your answer] - Submit your answer to the quiz\n/help - Show this message`;
    bot.sendMessage(chatId, helpMessage);
});
