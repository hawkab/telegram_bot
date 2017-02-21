# -*- coding: utf-8 -*-
#!/usr/bin/python
import config #файл с настройками
import telegram
import os
import subprocess
import sys
import shlex
import datetime
import MySQLdb

from time import sleep
from subprocess import Popen, PIPE
from telegram.ext import CommandHandler
from imp import reload #модуль для перезагрузки (обновления) других модулей

#bot = telegram.Bot(token = config.token)
#Проверка бота
#print(bot.getMe())
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

CHOOSING = range(1)

updater = Updater(token=config.token)
dispatcher = updater.dispatcher

def is_admin ( user ):
    return True if user in config.admin else False

def get_user ( update ):
    return update.message.from_user.id

def get_chat ( update ):
    return update.message.chat_id

def sql_exec ( request ):
    con = MySQLdb.connect("localhost","king","masterkey1","telegram_bot" )
    cur = con.cursor()
    cur.execute ( request )
    con.commit()
    result = cur.fetchall()
    con.close()

    return result

def store_chat ( update ):
    chat_id = get_chat ( update )
    user_id = get_user ( update )
    sql_exec ("INSERT INTO chat VALUES (%d, '%s' , '%s' , '%s', '%s', '%s')" \
        % ( chat_id 
            , update.message.chat.type 
            , update.message.chat.title 
            , update.message.chat.first_name 
            , update.message.chat.last_name
            , update.message.from_user.username ))
    
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
    /get_count_chats - получить общее число чатов
    /add_to_listeners - waiting for impl
    /add_to_admins - waiting for impl
    /send_to_all [текст] - отправка сообщения всем чатам
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

def send_to_all(bot, update):

    promo = update.message.text.strip().replace('/send_to_all', '').strip()
    if promo == '':
        bot.sendMessage( get_chat ( update ) , text='''Требуется ввести текст сообщения после команды 
/send_to_all Этот текст будет отправлен всем чатам''')
    else:
        reply_keyboard = [['Да', 'Нет']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        print 1
        update.message.reply_text("Вы уверены, что хотите отправить всем: %s?" % promo, reply_markup=markup)
        print 2



def send_to_all_confirm(bot, update, user_data):
    print update.message.text
    print user_data['choice'] 
    #chat_list = sql_exec ("SELECT * FROM chat")
    #    for chat in chat_list:
    #        bot.sendMessage(chat_id= chat[0] , text=promo)



def add_to_listeners(bot, update):
    userid = get_user ( update )
    bot.sendMessage(chat_id= get_chat ( update ) , text=userid)

def get_count_chats (bot, update):
    result = ""
    try:
        result = sql_exec ("SELECT COUNT(*) FROM chat")[0][0]
    except:
        result = "Ошибка выполнения запроса."
    bot.sendMessage(chat_id= get_chat ( update ) , text=result)
    
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

def cancel():
    pass

def main():


    send_to_all_confirm_bot_handler = RegexHandler('^(Да)$', send_to_all_confirm, pass_user_data=True)
    dispatcher.add_handler(send_to_all_confirm_bot_handler)

    restart_bot_handler = CommandHandler('restart_bot', restart_bot)
    dispatcher.add_handler(restart_bot_handler)

    add_to_listeners_handler = CommandHandler('add_to_listeners', add_to_listeners)
    dispatcher.add_handler(add_to_listeners_handler)

    add_to_admins_handler = CommandHandler('add_to_admins', add_to_admins)
    dispatcher.add_handler(add_to_admins_handler)

    get_count_chats_handler = CommandHandler('get_count_chats', get_count_chats)
    dispatcher.add_handler(get_count_chats_handler)

    send_to_all_handler = CommandHandler('send_to_all', send_to_all)
    dispatcher.add_handler(send_to_all_handler)

    df_handler = CommandHandler('df', df)
    dispatcher.add_handler(df_handler)

    free_handler = CommandHandler('free', free)
    dispatcher.add_handler(free_handler)


    myid_handler = CommandHandler('id', myid)
    dispatcher.add_handler(myid_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)


    updater.start_polling()

if __name__ == '__main__':
    main()