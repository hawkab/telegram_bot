# -*- coding: utf-8 -*-
#!/usr/bin/python
import telegram, os, subprocess, sys, shlex
import datetime, logging, config
from time import sleep
from subprocess import Popen, PIPE
from telegram.ext import CommandHandler
from imp import reload #модуль для перезагрузки (обновления) других модулей

from telegram import (ReplyKeyboardMarkup,ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)