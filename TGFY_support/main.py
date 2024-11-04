import telebot
import sqlite3

from telebot import types  # Импортируем модуль для работы с inline кнопками
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from googletrans import Translator 


# создание бот и подключение токена
bot = telebot.TeleBot('7023063772:AAFFbn8O4wnmyTaCDQnoDimkSC5KDLMeuw4')

# создание переводчика
trans = Translator()

# подключение бд и создание курсора
db = sqlite3.connect(r'E:\Python\TGFY_support\database.db', check_same_thread=False)
c = db.cursor()

# создание отношения пользователей
c.execute('''
          CREATE TABLE IF NOT EXISTS users (
          id INTEGER,
          user_name TEXT,
          lang TEXT,
          moderator INTEGER 
          )
          ''')

# создание отношения обращений
c.execute('''
          CREATE TABLE IF NOT EXISTS support (
          id INTEGER,
          user_name TEXT,
          topic TEXT,
          text TEXT,
          date DATE
          )
          ''')

# создание отношения модераторов [НЕРАБОТАЕТ]
c.execute('''
          CREATE TABLE IF NOT EXISTS moderators (
          id INTEGER UNIQUE,
          user_name TEXT,
          score INTEGER
          )
          ''')

# перевод текста
def trans_message(message, lang):
    translated_message = trans.translate(message, dest = lang)
    return translated_message.text

# проверка пользователя на регистрацию
def check_user(id):
    all_data = c.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchall()
    return all_data

# регистрация пользователя
def add_user(id, user_name, lang):
    c.execute('INSERT INTO users (id, user_name, lang) VALUES (?, ?, ?)', (id, user_name, lang))
    db.commit()

# проверка пользователя на статус модератора
def check_moderator(id):
    moderator_data = c.execute('SELECT moderator FROM users WHERE id = ?', (id,)).fetchone()
    return moderator_data[0]

# обновление языка пользователя на новый
def add_lang(lang, id):
    c.execute('UPDATE users SET lang = ? WHERE id = ?', (lang, id))
    db.commit()

# получение языка пользователя
def get_lang(id):
    lang = c.execute('SELECT lang FROM users WHERE id = ?', (id,)).fetchone()
    lang = lang[0]
    return lang

# добавление обращения пользователя
def add_text(id, text, topic, user_name):
    current_time = datetime.now().strftime('%H:%M %d-%m-%Y')
    c.execute('INSERT INTO support (id, user_name, topic, text, date) VALUES (?, ?, ?, ?, ?)', (id, user_name, topic, text, current_time))
    db.commit()


# ---------------------------------------------------------
# ПРИВЕТСТВЕННОЕ СООБЩЕНИЕ И ПЕРВОНАЧАЛЬНАЯ РАБОТА С БОТОМ
# ---------------------------------------------------------
@bot.message_handler(commands = ['start'])
def MAIN(message):
    id = message.from_user.id
    user_name = message.from_user.username
    if not check_user(id): # если пользователь незарегестрирован, ему предлагается выбрать язык 
        Mchose_lang = InlineKeyboardMarkup()
        Mchose_lang.row(InlineKeyboardButton('English', callback_data = 'lang_en'),
                        InlineKeyboardButton('Español', callback_data = 'lang_es'),
                        InlineKeyboardButton('Français', callback_data = 'lang_fr'),
                        InlineKeyboardButton('中文', callback_data = 'lang_zh-CN'),
                        InlineKeyboardButton('Русский', callback_data = 'lang_ru'))

        bot.send_message(id, 'Hello! 😊 I am the TGFY support bot! 🤖 To get started, choose your language. 🌍\nTo change the language, use the command /lang.\n\n¡Hola! 😊 ¡Soy el bot de soporte de TGFY! 🤖 Para comenzar, elige tu idioma. 🌍\nPara cambiar el idioma, usa el comando /lang.\n\nBonjour ! 😊 Je suis le bot de support TGFY ! 🤖 Pour commencer, choisissez votre langue. 🌍\nPour changer de langue, utilisez la commande /lang\n\n你好！😊 我是TGFY支持机器人！🤖 要开始，请选择您的语言。🌍\n要更改语言，请使用命令/lang。\n\nПривет! 😊 Я — бот поддержки TGFY! 🤖 Для начала работы, выбери свой язык. 🌍\nЧто бы изменить язык, используй команду /lang.', reply_markup = Mchose_lang)
    else:
        if check_moderator(id) == 1: # проверка на статус модератора
            id = message.from_user.id
            user_name = message.from_user.username
            Mmod_menu = InlineKeyboardMarkup()
            Mmod_menu.row(InlineKeyboardButton('Помощь', callback_data = 'helps'),
                          InlineKeyboardButton('Предложения', callback_data = 'sugs'))
            bot.send_message(id, 'Выбери блок обращений.', reply_markup = Mmod_menu)
        else:
            next_step(id)


# ----------------------------
# ИЗМЕНЕНИЕ ЯЗЫКА ПОЛЬЗОВАТЕЛЯ
# ----------------------------
@bot.message_handler(commands = ['lang', 'l', 'lan', 'ln', 'lg', 'lng'])
def lang(message):
    id = message.from_user.id
    Mchose_lang = InlineKeyboardMarkup()
    Mchose_lang.row(InlineKeyboardButton('English', callback_data = 'lang_en'),
                    InlineKeyboardButton('Español', callback_data = 'lang_es'),
                    InlineKeyboardButton('Français', callback_data = 'lang_fr'),
                    InlineKeyboardButton('中文', callback_data = 'lang_zh-CN'),
                    InlineKeyboardButton('Русский', callback_data = 'lang_ru'))
    bot.send_message(id, 'Choose a convenient language.\n\nElige un idioma conveniente.\n\n选择一个方便的语言。\n\nВыбери удобный язык.', reply_markup = Mchose_lang)


# выбор темы обращения пользователя
def next_step(id):
    Mchose_block = InlineKeyboardMarkup()
    Mchose_block.row(InlineKeyboardButton(trans_message('Помощь', get_lang(id)), callback_data = 'help'),
                    InlineKeyboardButton(trans_message('Предложение', get_lang(id)), callback_data = 'sug'))
    bot.send_message(id, trans_message('Привет! 😊 Я — бот поддержки TGFY!\n🤖 Здесь ты можешь задать нам вопрос или что-то предложить! 💬\n\nВыбери блок с темой обращения.', get_lang(id)), reply_markup = Mchose_block)

# принятие обращения пользователя
def process_user_message(message, id, topic, user_name):
    text = message.text
    if text != '/start': # если сообщение не /start, то происходит запись обращения 
        add_text(id, text, topic, user_name) # добавление обращения 
        Mchose_block = InlineKeyboardMarkup()
        Mchose_block.row(InlineKeyboardButton(trans_message('Помощь', get_lang(id)), callback_data = 'help'),
                         InlineKeyboardButton(trans_message('Предложение', get_lang(id)), callback_data = 'sug'))
        bot.send_message(id, trans_message('Ваше обращение принято, ожидайте ответа.\nЖдём, когда напишите снова :)', get_lang(id)), reply_markup = Mchose_block)
    else: # если пользователь пишет /start, бот не записывает его обращение
        next_step(id)


# -----------------------------------
# РАБОТА С ИНЛАЙН КНОПКАМИ МОДЕРАТОРА
# ----------------------------------- 
@bot.callback_query_handler(func=lambda call: call.data == 'helps')
def helps(call):
    id = call.from_user.id
    help_requests = c.execute('SELECT text, user_name, date FROM support WHERE topic = ?', ('Помощь',)).fetchall()
    response_text = "Вот все обращения по теме 'Помощь':\n\n"
    for text, user_name, date in help_requests:
        response_text += f"📝 {text}\n👤 Обратная связь: @{user_name}\n📅 Дата: {date}\n\n"  # Добавлены данные из столбца date и улучшен формат вывода
    bot.send_message(id, response_text)

@bot.callback_query_handler(func=lambda call: call.data == 'sugs')
def sugs(call):
    id = call.from_user.id
    help_requests = c.execute('SELECT text, user_name, date FROM support WHERE topic = ?', ('Предложение',)).fetchall()
    response_text = "Вот все обращения по теме 'Предложение':\n\n"
    for text, user_name, date in help_requests:
        response_text += f"📝 {text}\n👤 Обратная связь: @{user_name}\n📅 Дата: {date}\n\n"  # Добавлены данные из столбца date и улучшен формат вывода
    bot.send_message(id, response_text)

# -------------------------------------
# РАБОТА С ИНЛАЙН КНОПКАМИ ПОЛЬЗОВАТЕЛЯ
# ------------------------------------- 
@bot.callback_query_handler(func=lambda call: call.data == 'sug')
def sug(call):
    id = call.from_user.id
    user_name = call.from_user.username
    topic = 'Предложение'
    bot.send_message(id, trans_message('Напишите своё предложение и мы его рассмотрим.', get_lang(id)))
    bot.register_next_step_handler(call.message, process_user_message, id, topic, user_name)

@bot.callback_query_handler(func=lambda call: call.data == 'help')
def help(call):
    id = call.from_user.id
    user_name = call.from_user.username
    topic = 'Помощь'
    bot.send_message(id, trans_message('Опишите свою проблему и сторудник свяжется с вами в ближайшее время.', get_lang(id)))
    bot.register_next_step_handler(call.message, process_user_message, id, topic, user_name)

# ------------------------------
# ИНЛАЙН КНОПКА ДЛЯ ВЫБОРА ЯЗЫКА
# ------------------------------
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def chose_lang(call):
    id = call.from_user.id
    user_name = call.from_user.username
    lang = call.data.split('_')
    lang = lang[1]
    print(lang)
    if not check_user(id):
        add_user(id, user_name, lang)
    else:
        add_lang(lang, id)
    next_step(id)




if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()
