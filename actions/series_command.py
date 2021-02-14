# -*- coding: utf-8 -*-

from typing import List

from classes.ConvertBytes import HumanBytes
from classes.EZTV import ByIMDb, TorrentAvailable
from classes.OMDbAPI import SeriesByName
from classes.SeriesCommand import DisplayTorrentInformation, Options, SendInformation, TemplateInformation
from providers.EZTV import search_series_by_imdb
from providers.OMDbAPI import search_series_by_name
from resources.properties import EXTRA_QUALITY_OPTIONS, IMAGE_FORMAT, PLATFORMS, RESOLUTION_QUALITY, WEBRIP, WEB_DL
from src.logger import logger
from strings.series_command import INCORRECT_SERIES_FORMAT, NO_IMDB_ID_FOUND, NO_TORRENTS_FOUND, SEARCH_MOVIE_SERIES_COMMAND
from strings.series_command import SERIES_CAN_CONTAIN_SUBTITLES


def process_series_options(message: str) -> SendInformation:
    logger.info(f"Processing received message: {message}")

    series_name = ''
    season = ''
    episode = ''
    quality = ''

    parameters = message[8:].split('-')[1:]
    for parameter in parameters:
        parameter = parameter.strip()

        if parameter.startswith('n ') or parameter.startswith('name '):
            series_name = parse_name(parameter)
        elif parameter.startswith('s ') or parameter.startswith('season '):
            season = parse_season(parameter)
        elif parameter.startswith('e ') or parameter.startswith('episode '):
            episode = parse_episode(parameter)
        elif parameter.startswith('q ') or parameter.startswith('quality '):
            quality = parse_quality(parameter)

    if check_correct_parameters(series_name, season, episode, quality):
        options = Options(series_name, season, episode, quality)
        query_result = find_episode_torrents(options)
    else:
        query_result = SendInformation('', f"{INCORRECT_SERIES_FORMAT}")

    return query_result


def parse_name(parameter: str) -> str:
    name = ''

    if parameter.startswith('n '):
        name = parameter[2:]
    elif parameter.startswith('name '):
        name = parameter[5:]

    return name


def parse_season(parameter: str) -> str:
    raw_input = ''
    season = ''

    if parameter.startswith('s '):
        raw_input = parameter[2:]
    elif parameter.startswith('season '):
        raw_input = parameter[7:]

    if is_a_number(raw_input):
        season = raw_input

    return season


def parse_episode(parameter: str) -> str:
    raw_input = ''
    episode = ''

    if parameter.startswith('e '):
        raw_input = parameter[2:]
    elif parameter.startswith('episode '):
        raw_input = parameter[8:]

    if is_a_number(raw_input):
        episode = raw_input

    return episode


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


def check_correct_parameters(series_name: str, season: str, episode: str, quality: str) -> bool:
    return (series_name != '') and (season != '') and (episode != '') and (quality != '')


def find_episode_torrents(options: Options) -> SendInformation:
    logger.info(f"Finding IMDb series ID for: {options.series_name}")

    series_name = options.series_name
    search_result = search_series_by_name(series_name)
    if not search_result.is_empty() and search_result.is_series():
        template_information = find_series_torrents(options, search_result)
        if not template_information.is_empty():
            message = create_telegram_message(template_information)
            return message
        else:
            return SendInformation('', f"{NO_TORRENTS_FOUND}")
    elif search_result.error:
        return SendInformation('', f"{search_result.error_message}")
    elif not search_result.is_series():
        return SendInformation('', f"{SEARCH_MOVIE_SERIES_COMMAND}")
    else:
        return SendInformation('', f"{NO_IMDB_ID_FOUND}")


def find_series_torrents(options: Options, search_result: SeriesByName) -> TemplateInformation:
    logger.info(f"Finding torrents for: {options.series_name}")

    parsed_imdb_id = search_result.parsed_imdb_id
    poster_url = search_result.poster_url
    available_results = search_series_by_imdb(parsed_imdb_id)
    if not available_results.is_empty():
        filtered_torrents = filter_available_torrents(options, available_results)
        if filtered_torrents:
            template_information = TemplateInformation(poster_url, filtered_torrents)
            return template_information
        else:
            return TemplateInformation()
    else:
        return TemplateInformation()


def filter_available_torrents(options: Options, available_results: ByIMDb) -> List[DisplayTorrentInformation]:
    logger.info(f"Filtering torrents for: {options.series_name}")
    parsed_torrents = []

    torrents = available_results.torrents
    filtered_torrents = get_torrents_matches_user_options(options, torrents)
    if filtered_torrents:
        parsed_torrents = generate_display_information(options.quality, filtered_torrents)

    return parsed_torrents


def get_torrents_matches_user_options(options: Options, torrents: List[TorrentAvailable]) -> List[TorrentAvailable]:
    filtered_torrents = []

    for torrent in torrents:
        if options.season == torrent.season and options.episode == torrent.episode and torrent.title.find(options.quality) != -1:
            filtered_torrents.append(torrent)

    return filtered_torrents


def generate_display_information(quality: str, filtered_torrents: List[TorrentAvailable]) -> List[DisplayTorrentInformation]:
    logger.info(f"Analyzing data to show the information to the user.")
    result = []

    for filtered_torrent in filtered_torrents:
        raw_title = filtered_torrent.title
        title = get_title(quality, raw_title)
        season = filtered_torrent.season
        episode = filtered_torrent.episode
        image_quality = quality
        filename = filtered_torrent.filename
        file_type = get_file_type(filename)
        bytes_size = filtered_torrent.bytes_size
        size = HumanBytes.format(bytes_size, metric=True)
        seeds = filtered_torrent.seeds
        peers = filtered_torrent.peers
        health = get_health(seeds, peers)
        magnet_url = filtered_torrent.magnet_url
        torrent_url = filtered_torrent.torrent_url
        platform = ''
        release_type = ''
        subtitles = False
        scene = ''
        if quality != '480p':
            image_quality = get_image_quality(quality, raw_title)
            platform = get_platform(raw_title)
            release_type = get_release_type(raw_title)
            subtitles = can_contain_subtitles(release_type)
            scene = get_scene(raw_title)

        option = DisplayTorrentInformation(title, season, episode, image_quality, platform, release_type, subtitles, file_type, size, scene,
                                           health, magnet_url, torrent_url)
        result.append(option)

    return result


def get_title(quality: str, raw_title: str) -> str:
    logger.info(f"Recovering title.")

    index = raw_title.find(quality)
    title = raw_title[0:index]

    return title


def get_file_type(filename: str) -> str:
    logger.info(f"Recovering file type.")

    pieces = filename.split('.')
    file_format = pieces[-1].upper()

    return file_format


def get_health(seeds: int, peers: int) -> str:
    logger.info(f"Recovering health.")

    return f"{seeds} Seed(s) / {peers} Peer(s)"


def get_image_quality(quality: str, raw_title: str) -> str:
    logger.info(f"Recovering image quality.")
    result = quality

    for extra_quality_option in EXTRA_QUALITY_OPTIONS:
        if raw_title.find(extra_quality_option) != -1:
            result = result + f" {extra_quality_option}"

    return result


def get_platform(raw_title: str) -> str:
    logger.info(f"Recovering platform.")

    for abbreviation, name in PLATFORMS.items():
        if raw_title.find(abbreviation) != -1:
            return name

    return ''


def get_release_type(raw_title: str) -> str:
    logger.info(f"Recovering release type.")

    for name_type, options in IMAGE_FORMAT.items():
        for option in options:
            if raw_title.find(option) != -1:
                return option

    return ''


def can_contain_subtitles(release_type: str) -> bool:
    logger.info(f"Checking if it can contain subtitles.")

    return release_type in WEBRIP or release_type in WEB_DL


def get_scene(raw_title: str) -> str:
    logger.info(f"Recovering scene.")

    pieces = raw_title.split(' ')
    piece = pieces[-2]
    if '-' in piece:
        scene = piece.split('-')[1]
    else:
        scene = ''

    return scene


def create_telegram_message(template_information: TemplateInformation) -> SendInformation:
    logger.info(f"Generating message with format for Telegram.")

    torrents = template_information.torrents
    text_template = f""

    for index, torrent in enumerate(torrents, start=1):
        text_template = text_template + f"<strong><u>Option {index}</u></strong>\n"
        text_template = text_template + f"\n"
        text_template = text_template + f"<strong>Title:</strong> {torrent.title}\n"
        text_template = text_template + f"<strong>Season:</strong> {torrent.season}\n"
        text_template = text_template + f"<strong>Episode:</strong> {torrent.episode}\n"
        if torrent.platform != '':
            text_template = text_template + f"<strong>Platform:</strong> {torrent.platform}\n"
        text_template = text_template + f"<strong>Quality:</strong> {torrent.quality}\n"
        if torrent.release_type != '':
            text_template = text_template + f"<strong>Release type:</strong> {torrent.release_type}\n"
        if torrent.subtitles:
            text_template = text_template + f"<strong>Note:</strong> {SERIES_CAN_CONTAIN_SUBTITLES}\n"
        if torrent.scene != '':
            text_template = text_template + f"<strong>Scene:</strong> {torrent.scene}\n"
        text_template = text_template + f"<strong>File type:</strong> {torrent.file_type}\n"
        text_template = text_template + f"<strong>Size:</strong> {torrent.size}\n"
        text_template = text_template + f"<strong>Health:</strong> {torrent.health}\n"
        text_template = text_template + f"\U0001F5C3<strong>:</strong> <a title=\"Torrent File\" href=\"{torrent.torrent_url}\">" \
                                        f"Torrent File</a>\n"
        text_template = text_template + f"\n"

    poster_url = template_information.poster_url
    final_data = SendInformation(poster_url, text_template)

    return final_data
