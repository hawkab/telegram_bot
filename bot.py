# -*- coding: utf-8 -*-
#!/usr/bin/python

from common_func import *

global textoutput
updater = Updater(token=config.token)
dispatcher = updater.dispatcher

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

def main():

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSE: [RegexHandler('^(Да|да|ДА|lf)$',
                                    send_to_all_confirm,
                                    pass_user_data=True),
                       RegexHandler('^Нет$',
                                    cancel),
                       ],

            OTHER: [MessageHandler(Filters.text,
                                           cancel,
                                           pass_user_data=True),
                            ],
        },

        fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
    )

    dispatcher.add_handler(conv_handler)

    #send_to_all_confirm_handler = RegexHandler('^([Дд]|Да|да|ДА|lf)$', send_to_all_confirm, pass_user_data=True)
    #dispatcher.add_handler(send_to_all_confirm_handler)

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

    #start_handler = CommandHandler('start', start)
    #dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()