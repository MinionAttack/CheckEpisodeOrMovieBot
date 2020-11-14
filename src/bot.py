#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Press Ctrl-C on the command line or send a signal to the process to stop the bot.
"""

import html
import json
import traceback

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from src.command_handlers import echo, find_command, start_command, options_command
from resources.properties import BOT_TOKEN
from src.logger import logger


def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(msg=f"Exception while handling an update:", exc_info=context.error)


def configure_dispatcher(dispatcher):
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('options', options_command))
    dispatcher.add_handler(CommandHandler('find', find_command))

    # on no command message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Specify an error function to use when an error occurs
    dispatcher.add_error_handler(error_handler)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    configure_dispatcher(dispatcher)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
