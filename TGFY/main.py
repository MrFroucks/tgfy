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
db = sqlite3.connect('database.db', check_same_thread=False)
c = db.cursor()


c.execute('''
          CREATE TABLE IF NOT EXISTS users (
          id INTEGER,
          user_name TEXT,
          lang TEXT,
          topic TEXT,
          text TEXT,
          date DATE,
          moderator INTEGER 
          )
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS moderators (
          id INTEGER UNIQUE,
          user_name TEXT,
          score INTEGER
          )
          ''')

def trans_message(message, lang):
    translated_message = trans.translate(message, dest = lang)
    return translated_message.text

def check_user(id):
    all_data = c.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchall()
    return all_data

def add_user(id, user_name, lang):
    c.execute('INSERT INTO users (id, user_name, lang) VALUES (?, ?, ?)', (id, user_name, lang))
    db.commit()

def check_moderator(id):
    moderator_data = c.execute('SELECT moderator FROM users WHERE id = ?', (id,)).fetchone()
    return moderator_data[0]

def add_lang(lang, id):
    c.execute('UPDATE users SET lang = ? WHERE id = ?', (lang, id))
    db.commit()

def get_lang(id):
    lang = c.execute('SELECT lang FROM users WHERE id = ?', (id,)).fetchone()
    lang = lang[0]
    return lang

def add_text(id, text, topic):
    c.execute('UPDATE users SET topic = ?, text = ? WHERE id = ?', (topic, text, id))
    db.commit()

@bot.message_handler(commands = ['start'])
def MAIN(message):
    id = message.from_user.id
    user_name = message.from_user.username
    if not check_user(id):
        Mchose_lang = InlineKeyboardMarkup()
        Mchose_lang.row(InlineKeyboardButton('English', callback_data = 'en'),
                        InlineKeyboardButton('Español', callback_data = 'es'),
                        InlineKeyboardButton('Русский', callback_data = 'ru'))

        bot.send_message(id, 'Hello! 😊 I am the TGFY support bot! 🤖 To get started, choose your language. 🌍\nTo change the language, use the command /lang.\n\n¡Hola! 😊 ¡Soy el bot de soporte de TGFY! 🤖 Para comenzar, elige tu idioma. 🌍\nPara cambiar el idioma, usa el comando /lang.\n\nПривет! 😊 Я — бот поддержки TGFY! 🤖 Для начала работы, выбери свой язык. 🌍\nЧто бы изменить язык, используй команду /lang', reply_markup = Mchose_lang)
    else:
        if check_moderator(id) == 1:
            id = message.from_user.id
            user_name = message.from_user.username
            Mmod_menu = InlineKeyboardMarkup()
            Mmod_menu.row(InlineKeyboardButton('Помощь', callback_data = 'helps'),
                          InlineKeyboardButton('Предложения', callback_data = 'sugs'))
            bot.send_message(id, 'Выбери блок обращений.', reply_markup = Mmod_menu)
        else:
            next_step(id, user_name)

def next_step(id, user_name):
    Mchose_block = InlineKeyboardMarkup()
    Mchose_block.row(InlineKeyboardButton(trans_message('Помощь', get_lang(id)), callback_data = 'help'),
                    InlineKeyboardButton(trans_message('Предложение', get_lang(id)), callback_data = 'sug'))
    bot.send_message(id, trans_message('Привет! 😊 Я — бот поддержки TGFY!\n🤖 Здесь ты можешь задать нам вопрос или что-то предложить! 💬\n\nВыбери блок с темой обращения.', get_lang(id)), reply_markup = Mchose_block)

@bot.callback_query_handler(func=lambda call: call.data == 'helps')
def helps(call):
    id = call.from_user.id
    help_requests = c.execute('SELECT text, user_name FROM users WHERE topic = ?', ('Помощь',)).fetchall()
    response_text = "Вот все обращения по теме 'Помощь':\n\n"
    # Формируем текст ответа
    for text, user_name in help_requests:
        response_text += f"{text} (обратная связь: @{user_name})\n"
    bot.send_message(id, response_text)

@bot.callback_query_handler(func=lambda call: call.data == 'sugs')
def sugs(call):
    id = call.from_user.id
    help_requests = c.execute('SELECT text, user_name FROM users WHERE topic = ?', ('Предложение',)).fetchall()
    response_text = "Вот все обращения по теме 'Предложение':\n\n"
    # Формируем текст ответа
    for text, user_name in help_requests:
        response_text += f"{text} (обратная связь: @{user_name})\n"
    bot.send_message(id, response_text)

@bot.callback_query_handler(func=lambda call: call.data == 'sug')
def sug(call):
    id = call.from_user.id
    user_name = call.from_user.username
    topic = 'Предложение'
    bot.send_message(id, trans_message('Напишите своё предложение и мы его рассмотрим.', get_lang(id)))
    bot.register_next_step_handler(call.message, process_user_message, id, topic)

def process_user_message(message, id, topic):
    text = message.text
    add_text(id, text, topic)
    bot.send_message(id, trans_message('Ваше обращение принято, спасибо!', get_lang(id)))


@bot.callback_query_handler(func=lambda call: call.data == 'help')
def help(call):
    id = call.from_user.id
    user_name = call.from_user.username
    topic = 'Помощь'
    bot.send_message(id, trans_message('Опишите свою проблему и сторудник свяжется с вами в ближайшее время.', get_lang(id)))
    bot.register_next_step_handler(call.message, process_user_message, id, topic)

def process_user_message(message, id, topic):
    text = message.text
    add_text(id, text, topic)
    bot.send_message(id, trans_message('Ваше обращение принято, ожидайте ответа.', get_lang(id)))


@bot.callback_query_handler(func=lambda call: call.data == 'en')
def en(call):
    id = call.from_user.id
    user_name = call.from_user.username
    lang = 'en'
    if not check_user(id):
        add_user(id, user_name, lang)
    else:
        add_lang(lang, id)
    next_step(id, user_name)

@bot.callback_query_handler(func=lambda call: call.data == 'es')
def en(call):
    id = call.from_user.id
    user_name = call.from_user.username
    lang = 'es'
    if not check_user(id):
        add_user(id, user_name, lang)
    else:
        add_lang(lang, id)
    next_step(id, user_name)

@bot.callback_query_handler(func=lambda call: call.data == 'ru')
def en(call):
    id = call.from_user.id
    user_name = call.from_user.username
    lang = 'ru'
    if not check_user(id):
        add_user(id, user_name, lang)
    else:
        add_lang(lang, id)
    next_step(id, user_name)


if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()
