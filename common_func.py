# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
sys.path.insert(0, "/home/hawkab/telegram_bot/common_func.py")

from execSQL import *
from libraries import *

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