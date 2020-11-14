# -*- coding: utf-8 -*-

from telegram import Update
from telegram.ext import CallbackContext

from actions.find_command import process_find_options
from actions.options_command import get_options_details
from src.logger import logger
from strings.command_handlers import SEE_RESULTS, STATUS_COMMAND, WELCOME_START_COMMAND, WRONG_FORMAT_ECHO_COMMAND


def start_command(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message when the command /start is issued."""
    logger.info(f"Bot started for user: {update.message.from_user.username}")

    update.message.reply_text(WELCOME_START_COMMAND)


def status_command(update: Update, context: CallbackContext) -> None:
    """Sends a message to the user to check if the bot is running when the /status command is issued."""
    logger.info(f"Status check requested by user: {update.message.from_user.username}")

    update.message.reply_text(STATUS_COMMAND)


def options_command(update: Update, context: CallbackContext) -> None:
    """Sends a message of all available commands and how to use each of them when the /options command is issued."""
    logger.info(f"List of commands and how to use them requested by the user: {update.message.from_user.username}")

    options_details = get_options_details()
    update.message.reply_html(options_details)


def echo(update: Update, context: CallbackContext) -> None:
    """Sends a message when the user sends a no command."""
    logger.info(f"A no command has been sent from user: {update.message.from_user.username}")

    update.message.reply_text(WRONG_FORMAT_ECHO_COMMAND)


def find_command(update: Update, context: CallbackContext) -> None:
    """Sends a message when the user request to find an episode when the /find command is issued."""
    logger.info(f"Incoming search request from user: {update.message.from_user.username}")

    message = update.message.text.strip()
    available_options = process_find_options(message)

    logger.info(f"Sending results to the user: {update.message.from_user.username}")
    photo_url = available_options.photo_url
    caption = available_options.caption
    if photo_url != '' and caption != '':
        update.message.reply_photo(photo=photo_url, caption=SEE_RESULTS)
        update.message.reply_html(caption)
    elif caption != '':
        update.message.reply_text(caption)
