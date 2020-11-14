# -*- coding: utf-8 -*-
from src.logger import logger
from strings.options_command import FIND_COMMAND_TEXT, OPTIONS_COMMAND_TEXT, START_COMMAND_TEXT, STATUS_COMMAND_TEXT


def get_options_details() -> str:
    logger.info(f"Generating the text with the details of the commands.")

    start_command = generate_start_text()
    status_command = generate_status_text()
    options_command = generate_options_text()
    find_command = generate_find_text()

    full_text = f"{start_command}\n{status_command}\n{options_command}\n{find_command}"

    return full_text


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


def generate_options_text() -> str:
    logger.info(f"Generating options command text.")

    text = f"<strong><u>Options command</u></strong>\n"
    text = text + f"\n"
    text = text + OPTIONS_COMMAND_TEXT

    return text


def generate_find_text() -> str:
    logger.info(f"Generating find command text.")

    text = f"<strong><u>Find command</u></strong>\n"
    text = text + f"\n"
    text = text + FIND_COMMAND_TEXT

    return text
