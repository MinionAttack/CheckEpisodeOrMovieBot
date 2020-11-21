# -*- coding: utf-8 -*-
from resources.properties import AVAILABLE_HELP_COMMANDS
from src.logger import logger
from strings.help_command import INCORRECT_FORMAT_HELP, MOVIES_COMMAND_TEXT, HELP_COMMAND_TEXT, SERIES_COMMAND_TEXT, START_COMMAND_TEXT
from strings.help_command import STATUS_COMMAND_TEXT


def process_help_options(message: str) -> str:
    logger.info(f"Processing received message: {message}")

    parameters = message[6:].split('-')[1:]

    if not parameters:
        return HELP_COMMAND_TEXT
    else:
        command = ''
        for parameter in parameters:
            parameter = parameter.strip()

            if parameter.startswith('c ') or parameter.startswith('command '):
                command = parse_command(parameter)
                help_text = get_command_help(command)
                return help_text
            else:
                return INCORRECT_FORMAT_HELP


def parse_command(parameter: str) -> str:
    command = ''

    if parameter.startswith('c '):
        command = parameter[2:]
    elif parameter.startswith('command '):
        command = parameter[8:]

    return command


def get_command_help(command: str) -> str:
    logger.info(f"Getting help message for command: {command}")

    functions = {'start': generate_start_text(), 'status': generate_status_text(), 'help': generate_help_text(),
                 'series': generate_series_text(), 'movies': generate_movies_text()}

    if command in AVAILABLE_HELP_COMMANDS:
        command_help = functions[command]
        return command_help
    else:
        return INCORRECT_FORMAT_HELP


def generate_start_text() -> str:
    logger.info(f"Generating start command text.")

    text = f"<strong><u>Start command</u></strong>\n"
    text = text + f"\n"
    text = text + START_COMMAND_TEXT

    return text


def generate_status_text() -> str:
    logger.info(f"Generating status command text.")

    text = f"<strong><u>Status command</u></strong>\n"
    text = text + f"\n"
    text = text + STATUS_COMMAND_TEXT

    return text


def generate_help_text() -> str:
    logger.info(f"Generating help command text.")

    text = f"<strong><u>Help command</u></strong>\n"
    text = text + f"\n"
    text = text + HELP_COMMAND_TEXT

    return text


def generate_series_text() -> str:
    logger.info(f"Generating series command text.")

    text = f"<strong><u>Series command</u></strong>\n"
    text = text + f"\n"
    text = text + SERIES_COMMAND_TEXT

    return text


def generate_movies_text() -> str:
    logger.info(f"Generating movies command text.")

    text = f"<strong><u>Movies command</u></strong>\n"
    text = text + f"\n"
    text = text + MOVIES_COMMAND_TEXT

    return text
