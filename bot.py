# -*- coding: utf-8 -*-
#!/usr/bin/python
import config #файл с настройками
import telegram
import os
import subprocess
import sys
import shlex
import datetime
import sqlite3
from subprocess import Popen, PIPE
from telegram.ext import CommandHandler
from imp import reload #модуль для перезагрузки (обновления) других модулей

#bot = telegram.Bot(token = config.token)
#Проверка бота
#print(bot.getMe())
from telegram.ext import Updater
updater = Updater(token=config.token)
dispatcher = updater.dispatcher

def is_admin ( user ):
    return True if user in config.admin else False

def get_user ( update ):
    return update.message.from_user.id

def get_chat ( update ):
    return update.message.chat_id

def sql_exec ( request ):
    con = sqlite3.connect('/home/hawkab/telegram_bot/bot_store.db' , timeout=10)
    cur = con.cursor()
    cur.execute ( request )
    con.commit()
    result = cur.fetchall()
    con.close()
    
    return result

def store_chat ( update ):
    chat_id = get_chat ( update )
    user_id = get_user ( update )
    
    sql_exec ("INSERT INTO CHAT VALUES (%d, '%s' , '%s' , '%s', '%s')" \
        % ( chat_id 
            , update.message.chat.type 
            , update.message.chat.title 
            , update.message.chat.first_name 
            , update.message.chat.last_name ))
    print sql_exec (" select * from chat")
    
    

def get_count_usr():
    result = ""
    try:
        result = sql_exec ("SELECT COUNT(*) FROM CHAT")[0][0]
    except:
        result = "Ошибка выполнения запроса."
    return result 


#выполнение команды shell и вывод результата в телеграмм
def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    global textoutput
    textoutput = ''
    while True:
        global output
        output = process.stdout.readline()
        output = output.decode('utf8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print (output.strip())
        textoutput = textoutput + '\n' + output.strip()
    rc = process.poll()
    return rc
    

def start(bot, update):
    welcome_text ="Привет, я бот, жду команды. "
    welcome_text += get_help_text ( update )

    bot.sendMessage(chat_id= get_chat ( update ), text= welcome_text )
    store_chat ( update )

def get_help_text ( update ):
    reload(config)
    user = str ( get_user ( update ) )
    help_text = '''Список общедоступных команд: 
    /id - id пользователя'''
    help_text += '''
Список команд администратора:
    /df - информация о дисковом пространстве (df -h)
    /free - информация о памяти
    /get_count_users - получить общее число пользователей
    /add_to_listeners - waiting for impl
    /add_to_admins - waiting for impl
    /restart_bot - перезагрузка после обновления кода''' if is_admin ( user ) else ""
    return help_text

def help(bot, update):
    bot.sendMessage(chat_id= get_chat ( update ) , text = get_help_text ( update ) )

def myid(bot, update):
    userid = get_user ( update )
    bot.sendMessage(chat_id= get_chat ( update ) , text=userid)

def add_to_admins(bot, update):
    userid = get_user ( update )
    bot.sendMessage(chat_id= get_chat ( update ) , text=userid)

def add_to_listeners(bot, update):
    userid = get_user ( update )
    bot.sendMessage(chat_id= get_chat ( update ) , text=userid)

def get_count_users (bot, update):
    bot.sendMessage(chat_id= get_chat ( update ) , text=get_count_usr())
    
def restart_bot(bot, update):
    reload(config) 
    user = str ( get_user ( update ) )
    if is_admin ( user ): 
        run_command("systemctl restart telegram-bot.service && systemctl status telegram-bot.service")
        bot.sendMessage(chat_id= get_chat ( update ) , text=textoutput)

def df(bot, update):
    reload(config) 
    user = str ( get_user ( update ) )
    if is_admin ( user ): 
        run_command("df -h")
        bot.sendMessage(chat_id=get_chat ( update ) , text=textoutput)

def free(bot, update):
    reload(config) 
    user = str ( get_user ( update ) )
    if is_admin ( user ): 
        run_command("free -m")
        bot.sendMessage(chat_id= get_chat ( update ), text=textoutput)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

restart_bot_handler = CommandHandler('restart_bot', restart_bot)
dispatcher.add_handler(restart_bot_handler)

add_to_listeners_handler = CommandHandler('add_to_listeners', add_to_listeners)
dispatcher.add_handler(add_to_listeners_handler)

add_to_admins_handler = CommandHandler('add_to_admins', add_to_admins)
dispatcher.add_handler(add_to_admins_handler)

get_count_users_handler = CommandHandler('get_count_users', get_count_users)
dispatcher.add_handler(get_count_users_handler)

df_handler = CommandHandler('df', df)
dispatcher.add_handler(df_handler)

free_handler = CommandHandler('free', free)
dispatcher.add_handler(free_handler)


myid_handler = CommandHandler('id', myid)
dispatcher.add_handler(myid_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)


updater.start_polling()
