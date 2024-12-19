import telebot
import hashlib
from telebot import types
from secrets import secrets

# Создаем бота с вашим токеном
token = secrets.get('BOT_API_TOKEN')
bot = telebot.TeleBot(token)
user_state = {}

# Создаем основные меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🚀 Старт",)
    btn2 = types.KeyboardButton("❓ FAQ")
    markup.add(btn1, btn2)
    return markup

def what_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Хеширование")
    btn2 = types.KeyboardButton("Стеганография")
    btn3 = types.KeyboardButton("\U0001F519 Назад")
    markup.add(btn1, btn2, btn3)
    return markup

def hash_menu():
    markup = types.InlineKeyboardMarkup()
    btnMD5 = types.InlineKeyboardButton("MD5", callback_data='MD5')
    btnSHA1 = types.InlineKeyboardButton("SHA-1", callback_data='SHA1')
    markup.row(btnMD5, btnSHA1)
    btnSHA256 = types.InlineKeyboardButton("SHA-256", callback_data='SHA256')
    markup.row(btnSHA256)
    btnSHA224 = types.InlineKeyboardButton("SHA-224", callback_data='SHA224')
    btnSHA384 = types.InlineKeyboardButton("SHA-384", callback_data='SHA384')
    markup.row(btnSHA224, btnSHA384)
    btnSHA512 = types.InlineKeyboardButton("SHA-512", callback_data='SHA512')
    markup.row(btnSHA512)
    btnBlake2b = types.InlineKeyboardButton("blake2b", callback_data='blake2b')
    btnBlake2s = types.InlineKeyboardButton("blake2s", callback_data='blake2s')
    markup.row(btnBlake2b,btnBlake2s)
    return markup

def faq_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("\U0001F519 Назад")
    markup.add(btn1)
    return markup

# Обработчик команды хелп для выдачи справки о хешах
@bot.message_handler(commands=['help'])
def help_command(message):
    file= open('./priv.docx','rb')
    bot.send_document(message.chat.id, file)


#Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Привет, {0.first_name} 👋\nВоспользуйся кнопками\n🚀 Старт - для начала работы с ботом\n❓ FAQ - справка о боте".format(message.from_user),
        reply_markup=main_menu()
    )

#Обработчик текстовых сообщений
@bot.message_handler(content_types=["text", "audio", "document", "sticker", "video", "voice"])
def handle_text(message):
    if message.text == "🚀 Старт":
        bot.send_message(
            message.chat.id,
            "Выберите, что хотите делать:",
            reply_markup=what_menu()
        )

    elif message.text == "❓ FAQ":
        bot.send_message(
            message.chat.id,
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
                          "❗️PirateHat_bot ответственно относится к вашей конфиденциальности - бот не сохраняет и не распространяет личные данные. ❗️",
            parse_mode="HTML",reply_markup=faq_menu()
        )

    elif message.text == types.Sticker or message.text == types.Document or message.text == types.Audio\
            or message.text == types.Video or message.text == types.Voice:
        bot.send_message(message,"Пожалуйста, выберите опцию из меню:")

    elif message.text == "\U0001F519 Назад":
        bot.send_message(
            message.chat.id,
            "Вы вернулись в главное меню:",
            reply_markup=main_menu()
        )

    elif message.text == "Хеширование":
        bot.send_message(
            message.chat.id, "Выбери метод хеширования:",
            reply_markup = hash_menu())


    elif message.text == "Стеганография":
        bot.send_message(message.chat.id, "Последние новости: Сегодня отличный день!")

    else:
        bot.send_message(
            message.chat.id,
            "Извините, я вас не понял. Пожалуйста, выберите опцию из меню:",
            reply_markup=main_menu()
        )

#Обработчик Inline кнопок и переход к функциям хеширования
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    bot.send_message(callback.message.chat.id, "Скинь мне данные, а я их захеширую 😎")
    if callback.data == 'MD5':
        user_state[callback.message.chat.id] = 'MD5'  #Сохраняем выбор пользователя
        bot.register_next_step_handler(callback.message, hashingMd5)  #Ожидаем следующего сообщения

    elif callback.data == 'SHA1':
        user_state[callback.message.chat.id] = 'SHA1'
        bot.register_next_step_handler(callback.message, hashingSha1)

    elif callback.data == 'SHA224':
        user_state[callback.message.chat.id] = 'SHA224'
        bot.register_next_step_handler(callback.message, hashingSha224)

    elif callback.data == "SHA256":
        user_state[callback.message.chat.id] = 'SHA256'
        bot.register_next_step_handler(callback.message, hashingSha256)

    elif callback.data == "SHA384":
        user_state[callback.message.chat.id] = 'SHA384'
        bot.register_next_step_handler(callback.message, hashingSha384)

    elif callback.data == "SHA512":
        user_state[callback.message.chat.id] = 'SHA512'
        bot.register_next_step_handler(callback.message, hashingSha512)

    elif callback.data == "blake2b":
        user_state[callback.message.chat.id] = 'blake2b'
        bot.register_next_step_handler(callback.message, hashingBlake2b)

    elif callback.data == "blake2s":
        user_state[callback.message.chat.id] = 'blake2s'
        bot.register_next_step_handler(callback.message, hashingBlake2s)


#MD5
@bot.message_handler(content_types=["text", "audio", "document", "sticker", "voice"])
def hashingMd5(message):
    if message.content_type == 'text':
        user_message = message.text
        hasher = hashlib.md5()
        hasher.update(user_message.encode('utf-8'))  # Кодируем в UTF-8 перед хешированием
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили: {user_message}\nЕго MD5 хеш: {hex_hash}")

    elif message.content_type == 'sticker':
        file_info = bot.get_file(message.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.md5()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили стикер.\nЕго MD5 хеш: {hex_hash}")

    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.md5()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили документ.\nЕго SHA-1 хеш: {hex_hash}")

    elif message.content_type == 'audio':
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.md5()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили аудиофайл.\nЕго SHA-1 хеш: {hex_hash}")

    elif message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.md5()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили голосовое сообщение.\nЕго SHA-1 хеш: {hex_hash}")

    else:
        bot.send_message(message.chat.id,"Я могу работать с текстом, аудио, документами, стикерами и голосовыми сообщениями\n"
                                         "Пожалуйста, попробуйте снова :)")

#SHA-1
@bot.message_handler(content_types=["text", "audio", "document", "sticker", "voice"])
def hashingSha1(message):
    if message.content_type == 'text':
        user_message = message.text
        hasher = hashlib.sha1()
        hasher.update(user_message.encode('utf-8'))
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили: {user_message}\nЕго SHA-1 хеш: {hex_hash}")

    elif message.content_type == 'sticker':
        file_info = bot.get_file(message.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha1()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили стикер.\nЕго SHA-1 хеш: {hex_hash}")

    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha1()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили документ.\nЕго SHA-1 хеш: {hex_hash}")

    elif message.content_type == 'audio':
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha1()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили аудиофайл.\nЕго SHA-1 хеш: {hex_hash}")

    elif message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha1()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили голосовое сообщение.\nЕго SHA-1 хеш: {hex_hash}")

    else:
        bot.send_message(
            message.chat.id,
            "Я могу работать с текстом, аудио, документами, стикерами и голосовыми сообщениями\n"
            "Пожалуйста, попробуйте снова :)"
        )

#SHA224
@bot.message_handler(content_types=["text", "audio", "document", "sticker", "voice"])
def hashingSha224(message):
    if message.content_type == 'text':
        user_message = message.text
        hasher = hashlib.sha224()
        hasher.update(user_message.encode('utf-8'))
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили: {user_message}\nЕго SHA-224 хеш: {hex_hash}")

    elif message.content_type == 'sticker':
        file_info = bot.get_file(message.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha224()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили стикер.\nЕго SHA-224 хеш: {hex_hash}")

    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha224()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили документ.\nЕго SHA-224 хеш: {hex_hash}")

    elif message.content_type == 'audio':
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha224()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили аудиофайл.\nЕго SHA-224 хеш: {hex_hash}")

    elif message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha224()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили голосовое сообщение.\nЕго SHA-224 хеш: {hex_hash}")

    else:
        bot.send_message(
            message.chat.id,
            "Я могу работать с текстом, аудио, документами, стикерами и голосовыми сообщениями\n"
            "Пожалуйста, попробуйте снова :)"
        )

#SHA256
@bot.message_handler(content_types=["text", "audio", "document", "sticker", "voice"])
def hashingSha256(message):
    if message.content_type == 'text':
        user_message = message.text
        hasher = hashlib.sha256()
        hasher.update(user_message.encode('utf-8'))
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили: {user_message}\nЕго SHA-256 хеш: {hex_hash}")

    elif message.content_type == 'sticker':
        file_info = bot.get_file(message.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha256()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили стикер.\nЕго SHA-256 хеш: {hex_hash}")

    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha256()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили документ.\nЕго SHA-256 хеш: {hex_hash}")

    elif message.content_type == 'audio':
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha256()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили аудиофайл.\nЕго SHA-256 хеш: {hex_hash}")

    elif message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha256()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили голосовое сообщение.\nЕго SHA-256 хеш: {hex_hash}")

    else:
        bot.send_message(
            message.chat.id,
            "Я могу работать с текстом, аудио, документами, стикерами и голосовыми сообщениями\n"
            "Пожалуйста, попробуйте снова :)"
        )

#SHA384
@bot.message_handler(content_types=["text", "audio", "document", "sticker", "voice"])
def hashingSha384(message):
    if message.content_type == 'text':
        user_message = message.text
        hasher = hashlib.sha384()
        hasher.update(user_message.encode('utf-8'))
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили: {user_message}\nЕго SHA-384 хеш: {hex_hash}")

    elif message.content_type == 'sticker':
        file_info = bot.get_file(message.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha384()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили стикер.\nЕго SHA-384 хеш: {hex_hash}")

    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha384()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили документ.\nЕго SHA-384 хеш: {hex_hash}")

    elif message.content_type == 'audio':
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha384()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили аудиофайл.\nЕго SHA-384 хеш: {hex_hash}")

    elif message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha384()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили голосовое сообщение.\nЕго SHA-384 хеш: {hex_hash}")

    else:
        bot.send_message(
            message.chat.id,
            "Я могу работать с текстом, аудио, документами, стикерами и голосовыми сообщениями\n"
            "Пожалуйста, попробуйте снова :)"
        )

#SHA512
@bot.message_handler(content_types=["text", "audio", "document", "sticker", "voice"])
def hashingSha512(message):
    if message.content_type == 'text':
        user_message = message.text
        hasher = hashlib.sha512()
        hasher.update(user_message.encode('utf-8'))
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили: {user_message}\nЕго SHA-512 хеш: {hex_hash}")

    elif message.content_type == 'sticker':
        file_info = bot.get_file(message.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha512()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили стикер.\nЕго SHA-512 хеш: {hex_hash}")

    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha512()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили документ.\nЕго SHA-512 хеш: {hex_hash}")

    elif message.content_type == 'audio':
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha512()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили аудиофайл.\nЕго SHA-512 хеш: {hex_hash}")

    elif message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.sha512()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили голосовое сообщение.\nЕго SHA-512 хеш: {hex_hash}")

    else:
        bot.send_message(
            message.chat.id,
            "Я могу работать с текстом, аудио, документами, стикерами и голосовыми сообщениями\n"
            "Пожалуйста, попробуйте снова :)"
        )

#Blake2b
@bot.message_handler(content_types=["text", "audio", "document", "sticker", "voice"])
def hashingBlake2b(message):
    if message.content_type == 'text':
        user_message = message.text
        hasher = hashlib.blake2b()
        hasher.update(user_message.encode('utf-8'))
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили: {user_message}\nЕго blake2b хеш: {hex_hash}")

    elif message.content_type == 'sticker':
        file_info = bot.get_file(message.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.blake2b()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили стикер.\nЕго blake2b хеш: {hex_hash}")

    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.blake2b()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили документ.\nЕго blake2b хеш: {hex_hash}")

    elif message.content_type == 'audio':
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.blake2b()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили аудиофайл.\nЕго blake2b хеш: {hex_hash}")

    elif message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.blake2b()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили голосовое сообщение.\nЕго blake2b хеш: {hex_hash}")

    else:
        bot.send_message(
            message.chat.id,
            "Я могу работать с текстом, аудио, документами, стикерами и голосовыми сообщениями\n"
            "Пожалуйста, попробуйте снова :)"
        )

#Blake2s
@bot.message_handler(content_types=["text", "audio", "document", "sticker", "voice"])
def hashingBlake2s(message):
    if message.content_type == 'text':
        user_message = message.text
        hasher = hashlib.blake2s()
        hasher.update(user_message.encode('utf-8'))
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили: {user_message}\nЕго blake2s хеш: {hex_hash}")

    elif message.content_type == 'sticker':
        file_info = bot.get_file(message.sticker.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.blake2s()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили стикер.\nЕго blake2s хеш: {hex_hash}")

    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.blake2s()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили документ.\nЕго blake2s хеш: {hex_hash}")

    elif message.content_type == 'audio':
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.blake2s()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили аудиофайл.\nЕго blake2s хеш: {hex_hash}")

    elif message.content_type == 'voice':
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        hasher = hashlib.blake2s()
        hasher.update(downloaded_file)
        hex_hash = hasher.hexdigest()
        bot.reply_to(message, f"Вы отправили голосовое сообщение.\nЕго blake2s хеш: {hex_hash}")

    else:
        bot.send_message(
            message.chat.id,
            "Я могу работать с текстом, аудио, документами, стикерами и голосовыми сообщениями\n"
            "Пожалуйста, попробуйте снова :)"
        )

bot.polling(none_stop=True)
