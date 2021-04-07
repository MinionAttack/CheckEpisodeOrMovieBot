# -*- coding: utf-8 -*-

import datetime
from typing import List, Any

from classes.OMDbAPI import MovieByName
from classes.SubtitlesCommand import SendInformation, Options, DisplaySubtitleInformation
from classes.YIFY import ByIMDb
from providers.OMDbAPI import search_movie_by_name
from providers.YIFY import search_subtitles_by_imdb
from resources.properties import LANGUAGE_FLAG_CODES, SUBTITLES_LISTED_BY_DEFAULT
from src.logger import logger
from strings.subtitles_command import INCORRECT_SUBTITLES_FORMAT, LANGUAGE_NOT_AVAILABLE, NO_IMDB_ID_FOUND, NO_SUBTITLES_FOUND
from strings.subtitles_command import SEARCH_SERIES_SUBTITLE_COMMAND


def process_subtitles_options(message: str) -> SendInformation:
    logger.info(f"Processing received message: {message}")

    movie = ''
    year = datetime.datetime.now().year
    language_code = ''
    language = ''
    language_error = ''
    # Set default value
    limit = SUBTITLES_LISTED_BY_DEFAULT

    parameters = message[11:].split('-')[1:]
    for parameter in parameters:
        parameter = parameter.strip()

        if parameter.startswith('m ') or parameter.startswith('movie '):
            movie = parse_movie(parameter)
        elif parameter.startswith('y ') or parameter.startswith('year '):
            year = parse_year(parameter)
        elif parameter.startswith('la ') or parameter.startswith('language '):
            values = parse_language(parameter)
            language = values['language']
            language_code = values['language_code']
            language_error = values['error']
        elif parameter.startswith('li ') or parameter.startswith('limit '):
            limit = parse_limit(parameter)

    if check_correct_parameters(movie, year, language_code, language, limit) and (language_error != LANGUAGE_NOT_AVAILABLE):
        options = Options(movie, year, language_code, language, limit)
        query_result = find_movie_subtitles(options)
    elif language_error == LANGUAGE_NOT_AVAILABLE:
        query_result = SendInformation('', f"{LANGUAGE_NOT_AVAILABLE}")
    else:
        query_result = SendInformation('', f"{INCORRECT_SUBTITLES_FORMAT}")

    return query_result


def parse_movie(parameter: str) -> str:
    movie = ''

    if parameter.startswith('m '):
        movie = parameter[2:]
    elif parameter.startswith('movie '):
        movie = parameter[6:]

    return movie


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


def parse_language(parameter: str) -> dict:
    values = {'language': '', 'language_code': '', 'error': ''}
    raw_input = ''

    if parameter.startswith('la '):
        raw_input = parameter[3:]
    elif parameter.startswith('language '):
        raw_input = parameter[9:]

    specified_language = raw_input.lower()
    if specified_language in LANGUAGE_FLAG_CODES.keys():
        values['language'] = specified_language
        values['language_code'] = LANGUAGE_FLAG_CODES[specified_language]

        return values
    else:
        values['error'] = LANGUAGE_NOT_AVAILABLE

        return values


def parse_limit(parameter: str) -> int:
    raw_input = ''
    limit = -1

    if parameter.startswith('li '):
        raw_input = parameter[3:]
    elif parameter.startswith('limit '):
        raw_input = parameter[6:]

    if is_a_number(raw_input):
        limit = int(raw_input)

    return limit


def is_a_number(number: str) -> bool:
    try:
        int(number)
        return True
    except ValueError:
        return False


def check_correct_parameters(movie: str, year: int, language_code: str, language: str, limit: int) -> bool:
    return (movie != '') and (year is not None and year >= 0) and (language_code != '') and (language != '') and (limit >= 0)


def find_movie_subtitles(options: Options) -> SendInformation:
    logger.info(f"Finding IMDb movie ID for: {options.movie}")

    movie = options.movie
    year = options.year
    search_result = search_movie_by_name(movie, year)
    cover_url = search_result.poster_url
    if not search_result.is_empty() and search_result.is_movie():
        movie_subtitles = find_yify_subtitles(options, search_result)
        if movie_subtitles:
            template_information = generate_template_information(movie_subtitles)
            display_limit = options.limit
            message = generate_template(template_information, cover_url, display_limit)
            return message
        else:
            return SendInformation('', f"{NO_SUBTITLES_FOUND}")
    elif search_result.error:
        return SendInformation('', f"{search_result.error_message}")
    elif not search_result.is_movie():
        return SendInformation('', f"{SEARCH_SERIES_SUBTITLE_COMMAND}")
    else:
        return SendInformation('', f"{NO_IMDB_ID_FOUND}")


def find_yify_subtitles(options: Options, search_result: MovieByName) -> List[ByIMDb]:
    logger.info(f"Finding YIFY subtitles for: {options.movie}")

    imdb_id = search_result.imdb_id
    language = options.language
    available_results = search_subtitles_by_imdb(imdb_id, language)

    return available_results


def generate_template_information(movie_subtitles: List[ByIMDb]) -> List[DisplaySubtitleInformation]:
    logger.info('Generating template information.')

    template_information = []
    for movie_subtitle in movie_subtitles:
        rating_number = movie_subtitle.rating
        rating_text = process_rating_value(rating_number)
        language_text = movie_subtitle.language
        compatible_torrents_text = movie_subtitle.compatible_torrents
        uploader_text = movie_subtitle.uploader
        download_link_text = movie_subtitle.download_link

        option = DisplaySubtitleInformation(rating_text, language_text, compatible_torrents_text, uploader_text, download_link_text)
        template_information.append(option)

    return template_information


def process_rating_value(rating_number: int) -> str:

    if rating_number < 0:
        rating_text = f"{rating_number} \u274C"
    elif rating_number == 0:
        rating_text = f"{rating_number} \u26A0"
    else:
        rating_text = f"{rating_number} \u2705"

    return rating_text


def generate_template(template_information: List[DisplaySubtitleInformation], cover_url: str, display_limit: int) -> SendInformation:
    logger.info('Generating message with format for Telegram.')

    first_message = ''
    remaining_messages = []

    for index, movie_subtitle in enumerate(template_information, start=1):
        temp_text = ''
        if index <= display_limit:
            temp_text = temp_text + f"<strong><u>Option {index}</u></strong>\n"
            temp_text = temp_text + f"\n"
            temp_text = temp_text + f"<strong>Rating:</strong> {movie_subtitle.rating}\n"
            temp_text = temp_text + f"<strong>Language:</strong> {movie_subtitle.language}\n"
            temp_text = temp_text + f"<strong>Uploader:</strong> {movie_subtitle.uploader}\n"
            temp_text = temp_text + f"<strong>Compatible torrents:</strong>\n\n{movie_subtitle.compatible_torrents}\n\n"
            temp_text = temp_text + f"\U0001F5C3<strong>:</strong> <a title=\"Subtitle File\" href=\"{movie_subtitle.download_link}\">" \
                                    f"Subtitle File</a>\n"
            temp_text = temp_text + f"\n"

            exceeds_size = message_exceeds_size(first_message)
            if exceeds_size:
                remaining_messages.append(temp_text)
            else:
                first_message = first_message + temp_text
        else:
            break

    if remaining_messages:
        reduce_remaining_parts = join_remaining_parts(remaining_messages)
        result = SendInformation(cover_url, first_message, reduce_remaining_parts)
    else:
        result = SendInformation(cover_url, first_message)

    return result


def message_exceeds_size(text: str) -> bool:
    # The maximum number of characters in a message is 4096
    return len(text) > 4096


def join_remaining_parts(remaining_parts: List[str]) -> List[str]:
    result = []

    temp_text = ''
    for remaining_part in remaining_parts:
        exceeds_size = message_exceeds_size(temp_text)
        if not exceeds_size:
            temp_text = temp_text + remaining_part
        else:
            result.append(temp_text)
            temp_text = ''
            temp_text = temp_text + remaining_part

    return result
