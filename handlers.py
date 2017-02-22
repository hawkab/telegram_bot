# -*- coding: utf-8 -*-
#!/usr/bin/python

from common_func import *
CHOOSE, OTHER = range(2)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update):
    welcome_text ="Привет, я бот, жду команды. "
    welcome_text += get_help_text ( update )
    bot.sendMessage(chat_id= get_chat ( update ), text= welcome_text )
    try:
        store_chat ( update )
    except:
        pass
    return CHOOSE

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
        bot.sendMessage( get_chat ( update ) , text='''Требуется ввести текст сообщения после команды: 
/send_to_all Этот текст будет отправлен всем чатам''')
    else:
        reply_keyboard = [['Да', 'Нет']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text("Вы уверены, что хотите отправить всем?", reply_markup=markup)
        return CHOOSE

def send_to_all_confirm(bot, update, user_data):
    print 'enter in confirm'
    print update.message.text
    print user_data['choice'] 
    update.message.reply_text('Your %s? Yes, I would love to hear about that!' % text.lower())
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

def cancel(bot, update, user_data):
    print 'cancel'
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))