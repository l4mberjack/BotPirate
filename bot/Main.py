import telebot
import hashlib
from secrets import secrets
from telebot import types # для определения типов сообщений
from stegano import lsb

token = secrets.get('BOT_API_TOKEN')
bot = telebot.TeleBot(token)

# Хендлер и функция для обработки команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("🚀 Старт")
    faq_button = types.KeyboardButton("❓ FAQ")
    markup.add(start_button, faq_button)
    bot.send_message(message.chat.id, text="Привет, {0.first_name} 👋\nВоспользуйся кнопками\n🚀 Старт - для начала работы с ботом\n❓ FAQ - справка о боте".format(message.from_user), reply_markup=markup)

def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("🚀 Старт")
    faq_button = types.KeyboardButton("❓ FAQ")
    markup.add(start_button, faq_button)
    bot.send_message(message.chat.id, text="Главное меню\n🚀 Старт - для начала работы с ботом\n❓ FAQ - справка о боте",reply_markup=markup)


# Обработчик кнопок после /start
@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text == "🚀 Старт":
         bot.send_message(message.chat.id, "Давай хешировать!🤘", reply_markup=types.ReplyKeyboardRemove())
         main(message)
    elif message.text == "❓ FAQ":
         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
         faq_button = types.KeyboardButton("🔙 Назад")
         markup.add(faq_button)
         bot.send_message(message.chat.id, "Справка о боте:\n\n\tℹ️\n\tℹ️", reply_markup=markup)
    elif message.text == "🔙 Назад":
        menu(message)
    else:
        bot.send_message(message.chat.id,"Здесь я могу отвечать только на нажатие кнопок")


def main(message):
    markup = types.InlineKeyboardMarkup()
    btnText = types.InlineKeyboardButton("💬Текст💬",callback_data='Text')
    btnAudio = types.InlineKeyboardButton("🔊Аудио🔊",callback_data='Audio')
    markup.row(btnText, btnAudio)
    btnDocs = types.InlineKeyboardButton("📑Документ📑",callback_data='Docs')
    markup.row(btnDocs)
    btnStick = types.InlineKeyboardButton("🐹Стикер🐹",callback_data='Stick')
    btnVid = types.InlineKeyboardButton("🎦Видео🎦",callback_data='Video')
    markup.row(btnStick, btnVid)
    btnVoice = types.InlineKeyboardButton("🎤Голосовое сообщение🎤",callback_data='Voice')
    markup.row(btnVoice)
    btnBack = types.InlineKeyboardButton("🔙Назад🔙", callback_data='Back')
    markup.row(btnBack)
    bot.send_message(message.chat.id, "Выбери что будем хешировать:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'Back':
        menu(callback.message)

# бесконечное выполнение кода
bot.polling()