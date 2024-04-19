import telebot, asyncio, time


bot = telebot.TeleBot('5775063157:AAG4IWzRYUpTOlw8N8HY-wYYMgnOnObpiNA')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")