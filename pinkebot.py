#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import re
import json
import logging
import atexit
import configparser
import os

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PAYMENTS = {}
PRICE_CURRECY_REXP = re.compile(r'(\d+\.?\d*)\s*(\D+)?')

dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    with open(os.path.join(dir_path, 'payments.json')) as f:
        PAYMENTS = json.load(f)
except (ValueError, IOError):
    # Nothing to restore
    pass

def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text="I'm a bot, please talk to me!")

def price(update, context):
    text = update.message.text
    match = PRICE_CURRECY_REXP.search(text)

    price = match.group(1)
    currency = match.group(2) or ""
        
    try:
        price = float(price)
    except ValueError:
        context.bot.send_message(
            chat_id=update.message.chat_id, 
            text="Keine Nummer")
        return
    
    members = context.bot.get_chat_members_count(
        chat_id=update.message.chat_id
    ) - 1

    context.bot.send_message(
                chat_id=update.message.chat_id, 
                text="Pro Person: {:.2f} {}".format(
                    price/members,
                    currency
                    ))



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def save_state():
    with open(os.path.join(dir_path, "payments.json", "w")) as f:
        json.dump(PAYMENTS, f)

def main():
    config = configparser.ConfigParser()
    config.read(os.path.join(dir_path, 'config.ini'))
    token = config["API"]["token"]

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('preis', price))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    logger.info("Bot started.")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == "__main__":
    atexit.register(save_state)
    main()
