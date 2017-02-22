# -*- coding: utf-8 -*-
#!/usr/bin/python
import telegram, os, subprocess, sys, shlex
import datetime, MySQLdb, logging, config
from time import sleep
from subprocess import Popen, PIPE
from telegram.ext import CommandHandler
from imp import reload #модуль для перезагрузки (обновления) других модулей

#bot = telegram.Bot(token = config.token)
#Проверка бота
#print(bot.getMe())
from telegram import (ReplyKeyboardMarkup,ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)

sys.path.insert(0, "common_func")

from execSQL import *
from toast import * 
from mcolors import * 
from time import sleep
from setupcon import *


class Object():
	pass

def date2Str(input):
	return datetime.strftime(
		input
		, '%Y-%m-%d %H:%M:%S')

def getNow():
	return datetime.now()

def is_admin ( user ):
    return True if user in config.admin else False

def get_user ( update ):
    return update.message.from_user.id

def get_chat ( update ):
    return update.message.chat_id


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