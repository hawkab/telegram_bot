# -*- coding: utf-8 -*-
#!/usr/bin/python
import config #файл с настройками
import telegram
import os
import subprocess
import sys
import shlex
import datetime
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
    bot.sendMessage(chat_id=update.message.chat_id, text="Привет, я бот, жду команды.")

def help(bot, update):
    reload(config)
    user = str ( get_user ( update ) )
    help_message = '''Список общедоступных команд: 
    /id - id пользователя'''
    help_message += '''Список команд администратора:
    /df - информация о дисковом пространстве (df -h)
    /free - информация о памяти
    /mpstat - информация о нагрузке на процессор
    /restart_bot - перезагрузка после обновления кода''' if is_admin ( user ) else ""
    
    bot.sendMessage(chat_id=update.message.chat_id, text = help_message )

def myid(bot, update):
    userid = get_user ( update )
    bot.sendMessage(chat_id=update.message.chat_id, text=userid)
    
def restart_bot(bot, update):
    reload(config) 
    user = str ( get_user ( update ) )
    if is_admin ( user ): 
        run_command("systemctl restart telegram-bot.service && systemctl status telegram-bot.service")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

def df(bot, update):
    reload(config) 
    user = str ( get_user ( update ) )
    if is_admin ( user ): 
        run_command("df -h")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

def free(bot, update):
    reload(config) 
    user = str ( get_user ( update ) )
    if is_admin ( user ): 
        run_command("free -m")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

restart_bot_handler = CommandHandler('restart_bot', restart_bot)
dispatcher.add_handler(restart_bot_handler)

df_handler = CommandHandler('df', df)
dispatcher.add_handler(df_handler)

free_handler = CommandHandler('free', free)
dispatcher.add_handler(free_handler)


myid_handler = CommandHandler('id', myid)
dispatcher.add_handler(myid_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)


updater.start_polling()
