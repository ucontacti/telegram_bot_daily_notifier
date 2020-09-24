from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
# print(cg.get_price(ids='bitcoin', vs_currencies='usd'))

from config import TelegramToken

from telegram.ext import Updater
updater = Updater(token=TelegramToken, use_context=True)
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
from telegram.ext import CommandHandler, MessageHandler, Filters

import time
def start(update, context):
    while(True):
        context.bot.send_message(chat_id=update.message.chat_id, text=cg.get_price(ids='bitcoin', vs_currencies='usd'))
        time.sleep(3)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.message.chat_id, text=text_caps)

def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
updater.start_polling()