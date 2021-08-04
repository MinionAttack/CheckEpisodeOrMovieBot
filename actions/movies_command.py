# -*- coding: utf-8 -*-

import datetime

from classes.ConvertBytes import HumanBytes
from classes.MoviesCommand import DisplayMovieInformation, DisplayTorrentInformation, Options, SendInformation
from classes.OMDbAPI import MovieByName
from classes.YTS import ByIMDb
from providers.OMDbAPI import search_movie_by_name
from providers.YTS import search_movie_by_imdb
from resources.properties import IMAGE_FORMAT
from src.logger import logger
from src.utils import join_remaining_parts, message_exceeds_size, parse_name, parse_year, parse_quality
from strings.movies_command import INCORRECT_MOVIES_FORMAT, SEARCH_SERIES_MOVIE_COMMAND, NO_IMDB_ID_FOUND, NO_TORRENTS_FOUND


def process_movies_options(message: str) -> SendInformation:
    logger.info(f"Processing received message: {message}")

    movie_name = ''
    year = datetime.datetime.now().year
    quality = ''

    parameters = message[8:].split('-')[1:]
    for parameter in parameters:
        parameter = parameter.strip()

        if parameter.startswith('n ') or parameter.startswith('name '):
            movie_name = parse_name(parameter)
        elif parameter.startswith('y ') or parameter.startswith('year '):
            year = parse_year(parameter)
        elif parameter.startswith('q ') or parameter.startswith('quality '):
            quality = parse_quality(parameter)

    if check_correct_parameters(movie_name, year, quality):
        options = Options(movie_name, year, quality)
        query_result = find_movie_torrents(options)
    else:
        query_result = SendInformation('', f"{INCORRECT_MOVIES_FORMAT}")

    return query_result


def check_correct_parameters(movie_name: str, year: int, quality: str) -> bool:
    return (movie_name != '') and (year is not None and year >= 0) and (quality != '')


def find_movie_torrents(options: Options) -> SendInformation:
    logger.info(f"Finding IMDb movie ID for: {options.movie_name}")

    movie_name = options.movie_name
    year = options.year
    search_result = search_movie_by_name(movie_name, year)
    if not search_result.is_empty() and search_result.is_movie():
        movies_data = find_yts_torrents(options, search_result)
        if not movies_data.is_empty():
            template_information = generate_template_information(movies_data)
            message = generate_template(template_information)
            return message
        else:
            return SendInformation('', f"{NO_TORRENTS_FOUND}")
    elif search_result.error:
        return SendInformation('', f"{search_result.error_message}")
    elif not search_result.is_movie():
        return SendInformation('', f"{SEARCH_SERIES_MOVIE_COMMAND}")
    else:
        return SendInformation('', f"{NO_IMDB_ID_FOUND}")


def find_yts_torrents(options: Options, search_result: MovieByName) -> ByIMDb:
    logger.info(f"Finding YTS torrents for: {options.movie_name}")

    imdb_id = search_result.imdb_id
    quality_specified = options.quality
    available_results = search_movie_by_imdb(imdb_id, quality_specified)

    return available_results


def generate_template_information(movies_data: ByIMDb) -> DisplayMovieInformation:
    logger.info('Generating template information.')

    title = movies_data.title
    year = movies_data.year
    rating = f"{movies_data.rating} / 10"
    runtime = f"{movies_data.runtime} minute(s)"
    genres = movies_data.genres
    youtube_trailer = movies_data.youtube_trailer
    mpa_rating = movies_data.mpa_rating
    large_cover_image = movies_data.large_cover_image
    raw_torrents = movies_data.torrents

    torrents = []
    for torrent in raw_torrents:
        torrent_url = torrent.torrent_url
        quality = torrent.quality
        raw_release_type = torrent.release_type
        release_type = parse_release_type(raw_release_type)
        health = f"{torrent.seeds} Seed(s) / {torrent.peers} Peer(s)"
        size = HumanBytes.format(torrent.size_bytes, metric=True)

        option = DisplayTorrentInformation(torrent_url, quality, release_type, health, size)
        torrents.append(option)

    result = DisplayMovieInformation(title, year, rating, runtime, genres, youtube_trailer, mpa_rating, large_cover_image, torrents)

    return result


def parse_release_type(release_type: str) -> str:
    for options in IMAGE_FORMAT.values():
        for option in options:
            if option.lower() == release_type:
                return option

    return release_type


def generate_template(template_information: DisplayMovieInformation) -> SendInformation:
    logger.info('Generating message with format for Telegram.')

    torrents = template_information.torrents
    remaining_messages = []

    first_message = f"<strong>Title:</strong> {template_information.title}\n"
    first_message = first_message + f"<strong>Year:</strong> {template_information.year}\n"
    first_message = first_message + f"<strong>Genres:</strong> {template_information.genres}\n"
    first_message = first_message + f"<strong>Runtime:</strong> {template_information.runtime}\n"
    if template_information.mpa_rating != '':
        first_message = first_message + f"<strong>MPA rating:</strong> {template_information.mpa_rating}\n"
    first_message = first_message + f"<strong>IMDb rating:</strong> {template_information.rating}\n"
    first_message = first_message + f"\U0001F3A5<strong>:</strong> <a title=\"Movie Trailer\" href=\"" \
                                    f"{template_information.youtube_trailer}\">Movie Trailer</a>\n"
    first_message = first_message + f"\n"

    for index, torrent in enumerate(torrents, start=1):
        text_template = f"<strong><u>Option {index}</u></strong>\n"
        text_template = text_template + f"\n"
        text_template = text_template + f"<strong>Quality:</strong> {torrent.quality}\n"
        text_template = text_template + f"<strong>Release type:</strong> {torrent.release_type}\n"
        text_template = text_template + f"<strong>Size:</strong> {torrent.size}\n"
        text_template = text_template + f"<strong>Health:</strong> {torrent.health}\n"
        text_template = text_template + f"\U0001F5C3<strong>:</strong> <a title=\"Torrent File\" href=\"{torrent.torrent_url}\">" \
                                        f"Torrent File</a>\n"
        text_template = text_template + f"\n"

        exceeds_size = message_exceeds_size(first_message)
        if exceeds_size:
            remaining_messages.append(text_template)
        else:
            first_message = first_message + text_template

    cover_url = template_information.large_cover_image

    if remaining_messages:
        reduce_remaining_parts = join_remaining_parts(remaining_messages)
        result = SendInformation(cover_url, first_message, reduce_remaining_parts)
    else:
        result = SendInformation(cover_url, first_message)

    return result
