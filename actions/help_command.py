# -*- coding: utf-8 -*-

from resources.properties import AVAILABLE_HELP_COMMANDS
from src.logger import logger
from strings.help_command import INCORRECT_HELP_FORMAT, MOVIES_COMMAND_TEXT, HELP_COMMAND_TEXT, SERIES_COMMAND_TEXT, START_COMMAND_TEXT
from strings.help_command import STATUS_COMMAND_TEXT, SUBTITLES_COMMAND_TEXT


def process_help_options(message: str) -> str:
    logger.info(f"Processing received message: {message}")

    parameters = message[6:].split('-')[1:]

    if not parameters:
        return HELP_COMMAND_TEXT
    else:
        for parameter in parameters:
            parameter = parameter.strip()

            if parameter.startswith('c ') or parameter.startswith('command '):
                command = parse_command(parameter)
                help_text = get_command_help(command)
                return help_text
            else:
                return INCORRECT_HELP_FORMAT


def parse_command(parameter: str) -> str:
    command = ''

    if parameter.startswith('c '):
        command = parameter[2:]
    elif parameter.startswith('command '):
        command = parameter[8:]

    return command


def get_command_help(command: str) -> str:
    logger.info(f"Getting help message for command: {command}")

    if command in AVAILABLE_HELP_COMMANDS:
        if command == 'start':
            help_text = generate_start_text()
        elif command == 'status':
            help_text = generate_status_text()
        elif command == 'help':
            help_text = generate_help_text()
        elif command == 'series':
            help_text = generate_series_text()
        elif command == 'movies':
            help_text = generate_movies_text()
        elif command == 'subtitles':
            help_text = generate_subtitles_text()
        else:
            return INCORRECT_HELP_FORMAT

        return help_text
    else:
        return INCORRECT_HELP_FORMAT


def generate_start_text() -> str:
    logger.info('Generating start command text.')

    text = '<strong><u>Start command</u></strong>\n'
    text = text + '\n'
    text = text + START_COMMAND_TEXT

    return text


def generate_status_text() -> str:
    logger.info('Generating status command text.')

    text = '<strong><u>Status command</u></strong>\n'
    text = text + '\n'
    text = text + STATUS_COMMAND_TEXT

    return text


def generate_help_text() -> str:
    logger.info('Generating help command text.')

    text = '<strong><u>Help command</u></strong>\n'
    text = text + '\n'
    text = text + HELP_COMMAND_TEXT

    return text


def generate_series_text() -> str:
    logger.info('Generating series command text.')

    text = '<strong><u>Series command</u></strong>\n'
    text = text + '\n'
    text = text + SERIES_COMMAND_TEXT

    return text


def generate_movies_text() -> str:
    logger.info('Generating movies command text.')

    text = '<strong><u>Movies command</u></strong>\n'
    text = text + '\n'
    text = text + MOVIES_COMMAND_TEXT

    return text


def generate_subtitles_text() -> str:
    logger.info('Generating subtitles command text.')

    text = '<strong><u>Subtitles command</u></strong>\n'
    text = text + '\n'
    text = text + SUBTITLES_COMMAND_TEXT

    return text
