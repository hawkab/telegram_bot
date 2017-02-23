# -*- coding: utf-8 -*-
#!/usr/bin/python

from common_func import *
from handlers import *

updater = Updater(token=config.token)
dispatcher = updater.dispatcher

def main():

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSE: [RegexHandler('^(Да)$',
                                    send_to_all_confirm,
                                    pass_user_data=True),
                       RegexHandler('^(Нет)$',
                                    cancel,
                                    pass_user_data=True),
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