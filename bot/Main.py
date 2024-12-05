import telebot
import hashlib
from secrets import secrets
from telebot import types # для определения типов сообщений
from stegano import lsb

token = secrets.get('BOT_API_TOKEN')
bot = telebot.TeleBot(token)


def main(message):
    text = "Напиши в чат из списка метод хеширования:\n" \
           "• *md5*\n" \
           "• *sha1*\n" \
           "• *sha224*\n" \
           "• *sha256*\n" \
           "• *sha384*\n" \
           "• *sha512*\n" \
           "• *blake2b*\n" \
           "• *blake2s*"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


# Хендлер и функция для обработки команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("🚀 Старт")
    faq_button = types.KeyboardButton("❓ FAQ")
    markup.add(start_button, faq_button)
    bot.send_message(message.chat.id, text="Привет, {0.first_name} 👋\nВоспользуйся кнопками".format(message.from_user), reply_markup=markup)

# Обработчик кнопок после /start
@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == "🚀 Старт":
         bot.send_message(message.chat.id, "Давай хешировать!🤘")
         main(message)
    elif message.text == "❓ FAQ":
         bot.send_message(message.chat.id, "Справка о боте:\n\n\tℹ️\n\tℹ️")
    #else:
         #bot.send_message(message.chat.id,"Я могу отвечать только на нажатие кнопок")


# бесконечное выполнение кода
bot.polling()