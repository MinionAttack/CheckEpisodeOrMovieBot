# -*- coding: utf-8 -*-

from telegram import Update, User
from telegram.ext import CallbackContext

from actions.options_command import get_options_details
from actions.series_command import process_series_options
from src.logger import logger
from strings.command_handlers import SEE_RESULTS, STATUS_COMMAND, UNKNOWN_USER, WELCOME_START_COMMAND, WRONG_FORMAT_ECHO_COMMAND


def start_command(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message when the command /start is issued."""
    user_info = update.effective_message.from_user
    identifier = get_user(user_info)
    logger.info(f"Bot started for user: {identifier}")

    update.effective_message.reply_text(WELCOME_START_COMMAND)


def status_command(update: Update, context: CallbackContext) -> None:
    """Sends a message to the user to check if the bot is running when the /status command is issued."""
    user_info = update.effective_message.from_user
    identifier = get_user(user_info)
    logger.info(f"Status check requested by user: {identifier}")

    update.effective_message.reply_text(STATUS_COMMAND)


def options_command(update: Update, context: CallbackContext) -> None:
    """Sends a message of all available commands and how to use each of them when the /options command is issued."""
    user_info = update.effective_message.from_user
    identifier = get_user(user_info)
    logger.info(f"List of commands and how to use them requested by the user: {identifier}")

    options_details = get_options_details()
    update.effective_message.reply_html(options_details)


def echo(update: Update, context: CallbackContext) -> None:
    """Sends a message when the user sends a no command."""
    user_info = update.effective_message.from_user
    identifier = get_user(user_info)
    logger.info(f"A no command has been sent from user: {identifier}")

    update.effective_message.reply_text(WRONG_FORMAT_ECHO_COMMAND)


def series_command(update: Update, context: CallbackContext) -> None:
    """Sends a message when the user request to find an episode when the /series command is issued."""
    user_info = update.effective_message.from_user
    identifier = get_user(user_info)
    logger.info(f"Incoming search request from user: {identifier}")

    message = update.effective_message.text.strip()
    available_options = process_series_options(message)

    logger.info(f"Sending results to the user: {identifier}")
    photo_url = available_options.photo_url
    caption = available_options.caption
    if photo_url != '' and caption != '':
        update.effective_message.reply_photo(photo=photo_url, caption=SEE_RESULTS)
        update.effective_message.reply_html(caption)
    elif caption != '':
        update.effective_message.reply_text(caption)


def get_user(user: User) -> str:
    logger.info(f"Getting the user who sent the message.")

    full_name = user.full_name
    username = user.username

    if username is not None:
        return username
    elif full_name != '':
        return full_name
    else:
        return UNKNOWN_USER
