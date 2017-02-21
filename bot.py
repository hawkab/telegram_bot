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
    
#функция команады старт
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Привет, я бот, жду команды")

#функция команады help
def help(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    help_message = '''список доступных команд: 
    /id - id пользователя
    '''
    help_message += '''    /df - информация о дисковом пространстве (df -h)
    /free - информация о памяти
    /mpstat - информация о нагрузке на процессор''' if user in config.admin else ""
    
    bot.sendMessage(chat_id=update.message.chat_id, text = help_message )

#функция команады id
def myid(bot, update):
    userid = update.message.from_user.id
    bot.sendMessage(chat_id=update.message.chat_id, text=userid)
    

#функция команады ifconfig
def ifconfig(bot, update):
    reload(config) 
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("ifconfig")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#функция команады df
def df(bot, update):
    reload(config) 
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("df -h")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#функция команады free
def free(bot, update):
    reload(config) 
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("free -m")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#функция команады mpstat
def mpstat(bot, update):
    reload(config) 
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        run_command("mpstat")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)

#функция команады dir1
def dir1(bot, update):
    reload(config) 
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        dir1_command = "du -sh "+ config.dir1
        run_command(dir1_command)
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)
        
#функция команады dirbackup - проверяет наличие файла по дате
def dirbackup(bot, update):
    reload(config) 
    user = str(update.message.from_user.id)
    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
        now_date = datetime.date.today() # Текущая дата
        cur_year = str(now_date.year) # Год текущий
        cur_month = now_date.month # Месяц текущий
        if cur_month < 10:
            cur_month = str(now_date.month)
            cur_month = '0'+ cur_month
        else:
            cur_month = str(now_date.month)
        cur_day = str(now_date.day) # День текущий
        filebackup = config.dir_backup + cur_year + '-' + cur_month + '-' + cur_day + '.03.00.co.7z'  #формируем имя файла для поиска
        print (filebackup)
        filebackup_command = "ls -lh "+ filebackup
        run_command(filebackup_command)
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)
        

    
    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

ifconfig_handler = CommandHandler('ifconfig', ifconfig)
dispatcher.add_handler(ifconfig_handler)

df_handler = CommandHandler('df', df)
dispatcher.add_handler(df_handler)

free_handler = CommandHandler('free', free)
dispatcher.add_handler(free_handler)

mpstat_handler = CommandHandler('mpstat', mpstat)
dispatcher.add_handler(mpstat_handler)

dir1_handler = CommandHandler('dir1', dir1)
dispatcher.add_handler(dir1_handler)

dirbackup_handler = CommandHandler('dirbackup', dirbackup)
dispatcher.add_handler(dirbackup_handler)

myid_handler = CommandHandler('id', myid)
dispatcher.add_handler(myid_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)


updater.start_polling()
