import sys
my_file = open("id.txt", "r")
user_id = my_file.read()
my_file = open("time.txt", "r")
user_time = my_file.read()
import time
true_master = True
while true_master:
    named_tuple = time.localtime()
    time_string = time.strftime("%d/%m %H:%M", named_tuple)
    print (time_string)
    if time_string == user_time:
        true_master = False
    time.sleep(10)

import telebot #библиотека работы с ботами
print ('Бот в работе')
bot = telebot.TeleBot('1512353573:AAEgfg8N0-j43uuyiaySCtQrnfBbcyUNfgM') #Изменить токен на токен бота
k = 0
if k ==0:
    bot.send_message(user_id, 'Время пришло!')
    time.sleep(5)
    bot.send_message(user_id, 'Пора заниматься делами!')
    time.sleep(5)
    bot.send_message(user_id, 'Just do it!')
    sys.exit ()
bot.polling(none_stop=True)#Запуск бота
