# -*- coding: utf-8 -*-

from typing import List

from telegram import Update, User
from telegram.ext import CallbackContext

from actions.help_command import process_help_options
from actions.movies_command import process_movies_options
from actions.series_command import process_series_options
from actions.subtitles_command import process_subtitles_options
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


def help_command(update: Update, context: CallbackContext) -> None:
    """Sends a message of how to use a specific command when the /help command is issued."""
    user_info = update.effective_message.from_user
    identifier = get_user(user_info)
    logger.info(f"Help on how to use a command requested by the user: {identifier}")

    message = update.effective_message.text.strip()
    help_text = process_help_options(message)
    update.effective_message.reply_html(help_text)


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
    logger.info(f"(Series command) Incoming search request from user: {identifier}")

    message = update.effective_message.text.strip()
    available_options = process_series_options(message)

    photo_url = available_options.photo_url
    response_message = available_options.message
    send_message(update, identifier, photo_url, response_message)


def movies_command(update: Update, context: CallbackContext) -> None:
    """Sends a message when the user request to find a movie when the /movies command is issued."""
    user_info = update.effective_message.from_user
    identifier = get_user(user_info)
    logger.info(f"(Movies command) Incoming search request from user: {identifier}")

    message = update.effective_message.text.strip()
    available_options = process_movies_options(message)

    photo_url = available_options.photo_url
    response_message = available_options.message
    send_message(update, identifier, photo_url, response_message)


def subtitles_command(update: Update, context: CallbackContext) -> None:
    """Sends a message when the user request to find a subtitle for a movie when the /subtitles command is issued."""
    user_info = update.effective_message.from_user
    identifier = get_user(user_info)
    logger.info(f"(Subtitles command) Incoming search request from user: {identifier}")

    message = update.effective_message.text.strip()
    available_options = process_subtitles_options(message)

    photo_url = available_options.photo_url
    response_message = available_options.message
    remaining_messages = available_options.remaining_messages

    if not remaining_messages:
        send_message(update, identifier, photo_url, response_message)
    else:
        send_message(update, identifier, photo_url, response_message)
        send_remaining_messages(update, identifier, remaining_messages)


def get_user(user: User) -> str:
    logger.info('Getting the user who sent the message.')

    full_name = user.full_name
    username = user.username

    if username is not None:
        return username
    elif full_name != '':
        return full_name
    else:
        return UNKNOWN_USER


def send_message(update: Update, identifier: str, photo_url: str, message: str) -> None:
    logger.info(f"Sending results to the user: {identifier}")

    if photo_url != '' and message != '':
        update.effective_message.reply_photo(photo=photo_url, caption=SEE_RESULTS)
        update.effective_message.reply_html(message, disable_web_page_preview=True)
    elif message != '':
        update.effective_message.reply_text(message, disable_web_page_preview=True)


def send_remaining_messages(update: Update, identifier: str, remaining_messages: List[str]) -> None:
    logger.info(f"Sending remaining messages to the user: {identifier}")

    for remaining_message in remaining_messages:
        update.effective_message.reply_html(remaining_message, disable_web_page_preview=True)
