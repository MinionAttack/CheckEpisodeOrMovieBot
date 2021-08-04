# -*- coding: utf-8 -*-

from typing import Any, List

import requests

from resources.properties import RESOLUTION_QUALITY
from src.logger import logger


def handle_request(api_url: str, headers: Any, parameters: Any) -> Any:
    try:
        if headers is not None and parameters is not None:
            request = requests.get(api_url, headers=headers, params=parameters)
        elif parameters is None:
            request = requests.get(api_url, headers=headers)
        elif headers is None:
            request = requests.get(api_url, params=parameters)
        else:
            request = requests.get(api_url)
        request.raise_for_status()

        return request
    except requests.exceptions.HTTPError as http_error:
        logger.warning(f"Http Error: {http_error}")
    except requests.exceptions.ConnectionError as connection_error:
        logger.warning(f"Error Connecting: {connection_error}")
    except requests.exceptions.TooManyRedirects as redirects_error:
        logger.warning(f"Too Many Redirects: {redirects_error}")
    except requests.exceptions.Timeout as timeout_error:
        logger.warning(f"Timeout Error: {timeout_error}")
    except requests.exceptions.RequestException as request_exception:
        logger.warning(f"Error: {request_exception}")

    return None


def parse_name(parameter: str) -> str:
    name = ''

    if parameter.startswith('n '):
        name = parameter[2:]
    elif parameter.startswith('name '):
        name = parameter[5:]

    return name


def parse_year(parameter: str) -> Any:
    year = ''

    if parameter.startswith('y '):
        year = parameter[2:]
    elif parameter.startswith('year '):
        year = parameter[5:]

    if is_a_number(year):
        return int(year)
    else:
        return None


def parse_quality(parameter: str) -> str:
    raw_input = ''
    quality = ''

    if parameter.startswith('q '):
        raw_input = parameter[2:]
    elif parameter.startswith('quality '):
        raw_input = parameter[8:]

    if is_a_number(raw_input) and f"{raw_input}p" in RESOLUTION_QUALITY:
        quality = f"{raw_input}p"

    return quality


def is_a_number(number: str) -> bool:
    try:
        int(number)
        return True
    except ValueError:
        return False


# The maximum number of characters in a message is 4096
def message_exceeds_size(text: str) -> bool:
    return len(text) > 4096


def join_remaining_parts(remaining_parts: List[str]) -> List[str]:
    result = []

    number_remaining_parts = len(remaining_parts)
    temp_text = ''
    for index, remaining_part in enumerate(remaining_parts, start=1):
        temp_text = temp_text + remaining_part
        exceeds_size = message_exceeds_size(temp_text)
        if not exceeds_size:
            if index != number_remaining_parts:
                continue
            else:
                result.append(temp_text)
        else:
            result.append(temp_text)
            temp_text = '' + remaining_part

    return result
