from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

from config import TelegramToken

from telegram.ext import Updater
import datetime

updater = Updater(token=TelegramToken, use_context=True)
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
from telegram.ext import CommandHandler, MessageHandler, Filters

import time
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hellooo!!")

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.message.chat_id, text=text_caps)

def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def daily_job(update, context):
    """ Running on every day morning """
    t = datetime.time(8, 00, 00, 000000)
    # job_queue.run_repeating(notify_assignees, interval = 3, context=update)
    new_job = context.job_queue.run_daily(alarm, t, context=update.message.chat_id)
    context.chat_data['job'] = new_job

    update.message.reply_text('Notifier successfully set!')

def alarm(context):
    """Send the alarm message."""
    job = context.job
    text = cg.get_price(ids='bitcoin', vs_currencies='usd')["bitcoin"]["usd"]
    context.bot.send_message(job.context, text=text)

def unset(update, context):
    """Remove the job if the user changed their mind."""
    if 'job' not in context.chat_data:
        update.message.reply_text('You have no active notifier')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Notifier successfully unset!')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

daily = CommandHandler('notify', daily_job, pass_job_queue=True, pass_chat_data=True)
dispatcher.add_handler(daily)

dispatcher.add_handler(CommandHandler('unset', unset, pass_chat_data=True))

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()