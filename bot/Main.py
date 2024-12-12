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

#Менюшка c двумя кнопками
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
         whatDo(message)
    elif message.text == "❓ FAQ":
         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
         faq_button = types.KeyboardButton("🔙 Назад")
         markup.add(faq_button)
         bot.send_message(message.chat.id,
                          "Справка о боте:\nПривет!👋\n"
                          "Я PirateHat_bot🏴‍☠️- бот для работы с хешированием и стеганографией. Могу предложить тебе свою помощь:\n\n"
                          "🔐<b>Хеширование:</b>\n\n"
                          "• Вычисление хеша для текста, аудио, документа, стикера, видео или голосового сообщения "
                          "(выбери алгоритм: MD5, SHA-1, SHA-256, SHA-224, SHA-384, SHA-512, blake2b, blake2s – <i>подсказка*</i> по алгоритмам доступна). "
                          "Просто отправь мне данные - получи готовый хеш!\n\n"
                          "• Сравнить два хеша – проверь целостность данных. Загрузи два хеша, я проверю!\n\n"
                          "<i>*Напиши /help для получения подробной справки по каждому алгоритму.</i>\n\n"
                          "🏞️<b>Стеганография:</b>\n\n"
                          "• Спрятать секретное сообщение🤫 в картинке или аудио записи. Загрузи файл, отправь текст – готово!\n\n"
                          "• Извлечь скрытый текст из картинки или аудиофайла. Отправь файл, я извлеку информацию!\n\n\n"
                          "❗️PirateHat_bot ответственно относится к вашей конфиденциальности - бот не сохраняет и не распространяет личные данные. ❗️"
                          ,reply_markup=markup, parse_mode="HTML")

    elif message.text == "🔙 Назад":
        menu(message)



def whatDo(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    hash_button = types.KeyboardButton("Хеширование")
    steg_button = types.KeyboardButton("Стеганография")
    markup.add(hash_button, steg_button)
    bot.send_message(message.chat.id, "Давай выберем что будем делать!👨‍💻",reply_markup=markup)


def main(message):
    markup = types.InlineKeyboardMarkup()
    btnText = types.InlineKeyboardButton("💬Текст💬",callback_data='Text')
    btnAudio = types.InlineKeyboardButton("🔊Аудио🔊",callback_data='Audio')
    markup.row(btnText, btnAudio)
    btnDocs = types.InlineKeyboardButton("📑Документ📑",callback_data='Docs')
    markup.row(btnDocs)
    btnStick = types.InlineKeyboardButton("🐹Стикер🐹",callback_data='Sticker')
    btnVid = types.InlineKeyboardButton("🎦Видео🎦",callback_data='Video')
    markup.row(btnStick, btnVid)
    btnVoice = types.InlineKeyboardButton("🎤Голосовое сообщение🎤",callback_data='Voice')
    markup.row(btnVoice)
    btnBack = types.InlineKeyboardButton("🔙Назад🔙", callback_data='Back')
    markup.row(btnBack)
    bot.send_message(message.chat.id, "Выбери что будем хешировать:", reply_markup=markup, parse_mode="Markdown")


def hashing(message):
    bot.send_message(message.chat.id, "Скинь мне данные а я их захеширую 😎")
    if message.content_type == 'text':
        user_message = message.text
        hasher = hashlib.sha256()
        hasher.update(user_message.encode('utf-8'))  # Кодируем в UTF-8 перед хешированием
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили: {user_message}\nЕго SHA-256 хеш: {hex_hash}")
    # elif message.content_type == 'audio':


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'Text':
        chose_Data(callback.message)
    elif callback.data == 'Back':
        menu(callback.message)

@bot.message_handler(content_types=["text", "audio", "document", "sticker", "video", "voice"])
def chose_Data(message):
    bot.send_message(message.chat.id, "Скинь мне данные, а я их захеширую 😎")
    bot.register_next_step_handler(message, hashing)



# бесконечное выполнение кода
bot.polling()