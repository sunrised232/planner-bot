#!/usr/local/bin/python
import telebot #библиотека работы с ботами
import sqlite3
from re import *
import os
import random
global id
global db
global cur
global number
print ('Бот начал работу!')
bot = telebot.TeleBot('') #Требуется добавить ваш токен

#Фразы, которые бот отвечает, когда задача окончена
phrase =['Поздравляю, ты закончил задачу! LVL UP!', 'С этой закончили, возьмемся за другую? Твой уровень теперь выше!','Была задача, а теперь нет её! На шаг ближе к победе!']

#Подключение к базе данных
db = sqlite3.connect(r'case.db')
cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
                       cases TEXT,
                       id TEXT);
                            """)
db.commit()

cur.execute("SELECT * FROM users")

bd = cur.fetchmany(50)

#База данных lvl
lvl_db = sqlite3.connect(r'lvl.db')
lvl_cur = lvl_db.cursor()
lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                       cases TEXT,
                       id TEXT);
                            """)
lvl_db.commit()
lvl_cur.execute("SELECT * FROM users")
lvl_bd = lvl_cur.fetchmany(50)
if len(lvl_bd) == 0:
    lvl_complite = 0
    id_call = str(0)
    lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id_call))
    lvl_db.commit()

#back
@bot.message_handler(commands=['back'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/view_cases')
    keyboard.row('/lvl')
    bot.send_message(message.chat.id, 'Продолжим?', reply_markup=keyboard)
    id =message.from_user.id
    return id

#start
@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/view_cases')
    keyboard.row('/lvl')
    bot.send_message(message.chat.id, 'Привет, я бот-планировщик!\nЯ могу держать в уме 15 задач', reply_markup=keyboard)#\nТакже ты можешь поставить будильник введя дату и время в виде дд/мм чч:мм\nПопробуем?
    id =message.from_user.id
    return id

#-lvl
@bot.message_handler(commands=['-lvl'])
def start_message(message):
    id =str(message.from_user.id)
    lvl_db = sqlite3.connect(r'lvl.db')
    lvl_cur = lvl_db.cursor()
    lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                           cases TEXT,
                           id TEXT);
                                """)

    lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
    lvl_bd = lvl_cur.fetchmany(50)
    if len(lvl_bd)== 0:
        plus_lvl_bd = -1
        lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (plus_lvl_bd,id))
        lvl_db.commit()
        bot.send_message(message.chat.id, 'У тебя не было уровня, но теперь он равен -1')
    else:
        minus_lvl_bd = str(int(lvl_bd[0][0]) - 1)
        prev_lvl = lvl_bd[0][0]
        lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
        lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (minus_lvl_bd,id))
        lvl_db.commit()
        bot.send_message(message.chat.id, 'Надеюсь для этого была веская причина!')

#+lvl
@bot.message_handler(commands=['+lvl'])
def start_message(message):
    id =str(message.from_user.id)
    lvl_db = sqlite3.connect(r'lvl.db')
    lvl_cur = lvl_db.cursor()
    lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                           cases TEXT,
                           id TEXT);
                                """)

    lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
    lvl_bd = lvl_cur.fetchmany(50)
    
    if len(lvl_bd)== 0:
        plus_lvl_bd = 1
        lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (plus_lvl_bd,id))
        lvl_db.commit()
        bot.send_message(message.chat.id, 'У тебя не было уровня, но теперь он равен 1')
        
    else:
        plus_lvl_bd = str(int(lvl_bd[0][0]) + 1)
        prev_lvl = lvl_bd[0][0]
        lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
        lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (plus_lvl_bd,id))
        lvl_db.commit()
        bot.send_message(message.chat.id, 'Теперь твой уровень стал выше!')
    
#help
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я могу:\n 1) /view_cases - посмотреть задачи\n 2) Добавить задачу можно просто написав в меня')
    bot.send_message(message.chat.id, 'Для установки будильника напишите дату и время в виде дд/мм чч:мм')
    id =message.from_user.id
    return id

#lvl
@bot.message_handler(commands=['lvl'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/-lvl')
    keyboard.row('/+lvl')
    keyboard.row('/check_lvl')
    keyboard.row('/back')
    bot.send_message(message.chat.id, 'Что ты хочешь сделать со своим уровнем?', reply_markup=keyboard)

#check_lvl    
@bot.message_handler(commands=['check_lvl'])
def start_message(message):
    id =str(message.from_user.id)
    lvl_db = sqlite3.connect(r'lvl.db')
    lvl_cur = lvl_db.cursor()
    lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                           cases TEXT,
                           id TEXT);
                                """)

    lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
    lvl_bd = lvl_cur.fetchmany(50)
    lvl_db.commit()
    if len(lvl_bd) != 0:
        bot.send_message(message.chat.id, 'Твой уровень: ' + str(lvl_bd[0][0]))
    else:
        bot.send_message(message.chat.id, 'У тебя пока что нет уровня!')


#Посмотреть задачи Inline ответчик
@bot.message_handler(commands=['view_cases'])
def start_message(message):
    id =message.from_user.id
    db = sqlite3.connect(r'case.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                           cases TEXT,
                           id TEXT);
                                """)
    db.commit()
    cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
    bd = cur.fetchmany(50)
    if len (bd) == 0:
        bot.send_message(message.chat.id, text="У вас пока что нет дел!\nЧтобы добавить, напишите его мне:")
        
    elif len(bd) == 1:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))#callback_data - что передано при нажатии
        bot.send_message(message.chat.id, text="На сегодня есть 1 дело:", reply_markup=markup)
        
    elif len(bd) == 2:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 2 дела:", reply_markup=markup)
        
    elif len(bd) == 3:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 3 дела:", reply_markup=markup)
        
    elif len(bd) == 4:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='4) ' + bd[3][0], callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 4 дела:", reply_markup=markup)
        
    elif len(bd) == 5:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='4) ' + bd[3][0], callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='5) ' + bd[4][0], callback_data=5))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 5 дел:", reply_markup=markup)
        
    elif len(bd) == 6:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='4) ' + bd[3][0], callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='5) ' + bd[4][0], callback_data=5))
        markup.add(telebot.types.InlineKeyboardButton(text='6) ' + bd[5][0], callback_data=6))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 6 дел:", reply_markup=markup)
        
    elif len(bd) == 7:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='4) ' + bd[3][0], callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='5) ' + bd[4][0], callback_data=5))
        markup.add(telebot.types.InlineKeyboardButton(text='6) ' + bd[5][0], callback_data=6))
        markup.add(telebot.types.InlineKeyboardButton(text='7) ' + bd[6][0], callback_data=7))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 7 дел:", reply_markup=markup)
        
    elif len(bd) == 8:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='4) ' + bd[3][0], callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='5) ' + bd[4][0], callback_data=5))
        markup.add(telebot.types.InlineKeyboardButton(text='6) ' + bd[5][0], callback_data=6))
        markup.add(telebot.types.InlineKeyboardButton(text='7) ' + bd[6][0], callback_data=7))
        markup.add(telebot.types.InlineKeyboardButton(text='8) ' + bd[7][0], callback_data=8))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 8 дел:", reply_markup=markup)
        
    elif len(bd) == 9:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='4) ' + bd[3][0], callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='5) ' + bd[4][0], callback_data=5))
        markup.add(telebot.types.InlineKeyboardButton(text='6) ' + bd[5][0], callback_data=6))
        markup.add(telebot.types.InlineKeyboardButton(text='7) ' + bd[6][0], callback_data=7))
        markup.add(telebot.types.InlineKeyboardButton(text='8) ' + bd[7][0], callback_data=8))
        markup.add(telebot.types.InlineKeyboardButton(text='9) ' + bd[8][0], callback_data=9))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 9 дел:", reply_markup=markup)
        
    elif len(bd) == 10:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='4) ' + bd[3][0], callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='5) ' + bd[4][0], callback_data=5))
        markup.add(telebot.types.InlineKeyboardButton(text='6) ' + bd[5][0], callback_data=6))
        markup.add(telebot.types.InlineKeyboardButton(text='7) ' + bd[6][0], callback_data=7))
        markup.add(telebot.types.InlineKeyboardButton(text='8) ' + bd[7][0], callback_data=8))
        markup.add(telebot.types.InlineKeyboardButton(text='9) ' + bd[8][0], callback_data=9))
        markup.add(telebot.types.InlineKeyboardButton(text='10) ' + bd[9][0], callback_data=10))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 10 дел:", reply_markup=markup)
        
    elif len(bd) == 11:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='4) ' + bd[3][0], callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='5) ' + bd[4][0], callback_data=5))
        markup.add(telebot.types.InlineKeyboardButton(text='6) ' + bd[5][0], callback_data=6))
        markup.add(telebot.types.InlineKeyboardButton(text='7) ' + bd[6][0], callback_data=7))
        markup.add(telebot.types.InlineKeyboardButton(text='8) ' + bd[7][0], callback_data=8))
        markup.add(telebot.types.InlineKeyboardButton(text='9) ' + bd[8][0], callback_data=9))
        markup.add(telebot.types.InlineKeyboardButton(text='10) ' + bd[9][0], callback_data=10))
        markup.add(telebot.types.InlineKeyboardButton(text='11) ' + bd[10][0], callback_data=11))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 11 дел:", reply_markup=markup)
        
    elif len(bd) == 12:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='4) ' + bd[3][0], callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='5) ' + bd[4][0], callback_data=5))
        markup.add(telebot.types.InlineKeyboardButton(text='6) ' + bd[5][0], callback_data=6))
        markup.add(telebot.types.InlineKeyboardButton(text='7) ' + bd[6][0], callback_data=7))
        markup.add(telebot.types.InlineKeyboardButton(text='8) ' + bd[7][0], callback_data=8))
        markup.add(telebot.types.InlineKeyboardButton(text='9) ' + bd[8][0], callback_data=9))
        markup.add(telebot.types.InlineKeyboardButton(text='10) ' + bd[9][0], callback_data=10))
        markup.add(telebot.types.InlineKeyboardButton(text='11) ' + bd[10][0], callback_data=11))
        markup.add(telebot.types.InlineKeyboardButton(text='12) ' + bd[11][0], callback_data=12))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 12 дел:", reply_markup=markup)
        
    elif len(bd) == 13:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='4) ' + bd[3][0], callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='5) ' + bd[4][0], callback_data=5))
        markup.add(telebot.types.InlineKeyboardButton(text='6) ' + bd[5][0], callback_data=6))
        markup.add(telebot.types.InlineKeyboardButton(text='7) ' + bd[6][0], callback_data=7))
        markup.add(telebot.types.InlineKeyboardButton(text='8) ' + bd[7][0], callback_data=8))
        markup.add(telebot.types.InlineKeyboardButton(text='9) ' + bd[8][0], callback_data=9))
        markup.add(telebot.types.InlineKeyboardButton(text='10) ' + bd[9][0], callback_data=10))
        markup.add(telebot.types.InlineKeyboardButton(text='11) ' + bd[10][0], callback_data=11))
        markup.add(telebot.types.InlineKeyboardButton(text='12) ' + bd[11][0], callback_data=12))
        markup.add(telebot.types.InlineKeyboardButton(text='13) ' + bd[12][0], callback_data=13))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 13 дел:", reply_markup=markup)
        
    elif len(bd) == 14:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='4) ' + bd[3][0], callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='5) ' + bd[4][0], callback_data=5))
        markup.add(telebot.types.InlineKeyboardButton(text='6) ' + bd[5][0], callback_data=6))
        markup.add(telebot.types.InlineKeyboardButton(text='7) ' + bd[6][0], callback_data=7))
        markup.add(telebot.types.InlineKeyboardButton(text='8) ' + bd[7][0], callback_data=8))
        markup.add(telebot.types.InlineKeyboardButton(text='9) ' + bd[8][0], callback_data=9))
        markup.add(telebot.types.InlineKeyboardButton(text='10) ' + bd[9][0], callback_data=10))
        markup.add(telebot.types.InlineKeyboardButton(text='11) ' + bd[10][0], callback_data=11))
        markup.add(telebot.types.InlineKeyboardButton(text='12) ' + bd[11][0], callback_data=12))
        markup.add(telebot.types.InlineKeyboardButton(text='13) ' + bd[12][0], callback_data=13))
        markup.add(telebot.types.InlineKeyboardButton(text='14) ' + bd[13][0], callback_data=14))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 14 дел:", reply_markup=markup)
        
    elif len(bd) == 15:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='1) ' + bd[0][0], callback_data=1))#text - что отображено на кнопке
        markup.add(telebot.types.InlineKeyboardButton(text='2) ' + bd[1][0], callback_data=2))#callback_data - что передано при нажатии
        markup.add(telebot.types.InlineKeyboardButton(text='3) ' + bd[2][0], callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='4) ' + bd[3][0], callback_data=4))
        markup.add(telebot.types.InlineKeyboardButton(text='5) ' + bd[4][0], callback_data=5))
        markup.add(telebot.types.InlineKeyboardButton(text='6) ' + bd[5][0], callback_data=6))
        markup.add(telebot.types.InlineKeyboardButton(text='7) ' + bd[6][0], callback_data=7))
        markup.add(telebot.types.InlineKeyboardButton(text='8) ' + bd[7][0], callback_data=8))
        markup.add(telebot.types.InlineKeyboardButton(text='9) ' + bd[8][0], callback_data=9))
        markup.add(telebot.types.InlineKeyboardButton(text='10) ' + bd[9][0], callback_data=10))
        markup.add(telebot.types.InlineKeyboardButton(text='11) ' + bd[10][0], callback_data=11))
        markup.add(telebot.types.InlineKeyboardButton(text='12) ' + bd[11][0], callback_data=12))
        markup.add(telebot.types.InlineKeyboardButton(text='13) ' + bd[12][0], callback_data=13))
        markup.add(telebot.types.InlineKeyboardButton(text='14) ' + bd[13][0], callback_data=14))
        markup.add(telebot.types.InlineKeyboardButton(text='15) ' + bd[14][0], callback_data=15))
        markup.add(telebot.types.InlineKeyboardButton(text='отчистить все', callback_data=16))
        bot.send_message(message.chat.id, text="На сегодня есть 15 дел:", reply_markup=markup)
        return id

#Inline ответчик
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    
    id = call.from_user.id
    bot.answer_callback_query(callback_query_id=call.id, text='')
    answer = ''
    
    if call.data == '1':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[0][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '2':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[1][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()
            
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '3':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[2][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '4':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[3][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
        else:
            
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '5':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[4][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
        else:
            
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '6':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[5][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '7':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[6][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()

        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '8':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[7][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '9':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[8][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '10':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[9][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()
            
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '11':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[10][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()
            
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '12':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[11][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()
            
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '13':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[12][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '14':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[13][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        
    elif call.data == '15':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        bd = cur.fetchmany(50)
        cur.execute("DELETE FROM users WHERE cases=:cases",{'cases': bd[14][0]})
        db.commit()
        random_phrase = random.randint(0,2)
        answer = phrase[random_phrase]
        #Поднятие уровня
        lvl_db = sqlite3.connect(r'lvl.db')
        lvl_cur = lvl_db.cursor()
        lvl_cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        lvl_cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
        lvl_bd = lvl_cur.fetchmany(50)
        lvl_db.commit()
        
        if len(lvl_bd) == 0:
            lvl_complite = 0
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_complite, id))
            lvl_db.commit()
            
        else:
            lvl_up = str(int(lvl_bd[0][0]) + 1)
            lvl_cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
            lvl_cur.execute("INSERT INTO users VALUES(?, ?)", (lvl_up, id))
            lvl_db.commit()

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    elif call.data == '16':
        db = sqlite3.connect(r'case.db')
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                               cases TEXT,
                               id TEXT);
                                    """)
        cur.execute("DELETE FROM users WHERE id=:id",{'id': id})
        db.commit()
        answer = 'Все чисто!'
    bot.send_message(call.message.chat.id, answer)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    return id

#Добавление новой задачи
@bot.message_handler(content_types=['text'])
def send_text(message):
    q = 0
    id =message.from_user.id
    id_u = message.from_user.id
    db = sqlite3.connect(r'case.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                            cases TEXT,
                            id TEXT);
                                """)
    cur.execute("SELECT * FROM users WHERE id=:id",{'id': id})
    bd = cur.fetchmany(50)

    pattern = compile('[0-3][0-9]/[0-1][0-9] [0-2][0-9]:[0-5][0-9]')
    cases_input = message.text
    is_valid = pattern.match(cases_input)
    if is_valid:
        my_file = open("id.txt", "w+")
        my_file.write(str(id))
        my_file.close()
        my_file = open("time.txt", "w+")
        time_mes =message.text
        my_file.write(time_mes)
        my_file.close()
        bot.send_message(message.chat.id, 'Будильник установлен!')
        os.startfile('main2.py')
        q = 1


    pattern = compile('.{1,33}')
    cases_input = message.text
    is_valid = pattern.match(cases_input)
    
    if is_valid and q ==0:
        cases_compile = is_valid.group()
        bd_wtht_second = []
        
        for i in range (len(bd)):
            bd_wtht_second.append (bd[i][0])
            
        if cases_compile not in bd_wtht_second:
            
            if len (bd)<15:
                db = sqlite3.connect(r'case.db')
                cur = db.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                       cases TEXT,
                                       id TEXT);
                                            """)
                cur.execute("INSERT INTO users VALUES(?, ?)", (cases_compile,id))
                db.commit()
                bot.send_message(message.chat.id, 'Задача добавлена!')
                
            else:
                bot.send_message(message.chat.id, 'У меня не может быть столько задач!\nУдали из меня что-нибудь, пожалуйста(((')
                
        else:
            bot.send_message(message.chat.id, 'Такая задача уже существует!')

        return id
    

bot.polling(none_stop=True)#Запуск бота
