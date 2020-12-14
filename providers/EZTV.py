# -*- coding: utf-8 -*-

from math import ceil
from typing import Any, List

import requests

from classes.EZTV import ByIMDb, TorrentAvailable
from src.logger import logger

EZTV_API = 'https://eztv.re/api/get-torrents'
# Results per page, between 1 and 100
LIMIT = 100
INITIAL_PAGE = 1


def search_series_by_imdb(series_id: str) -> ByIMDb:
    payload = {'limit': LIMIT, 'page': INITIAL_PAGE, 'imdb_id': series_id}
    request = handle_request(EZTV_API, payload)

    if (request is not None) and (request.status_code == 200):
        json_object = request.json()

        imdb_id = json_object['imdb_id']
        torrents_count = json_object['torrents_count']
        if torrents_count > 0:
            torrents = json_object['torrents']
            pages = measure_number_pages(torrents_count)

            if pages > 1:
                total_torrents = requests_remaining_pages(series_id, pages, torrents)
            else:
                total_torrents = torrents

            parsed_torrents = parse_available_torrents(total_torrents)
            result = ByIMDb(imdb_id, torrents_count, parsed_torrents)

            return result
        else:
            logger.warning(f"No results for the series with IMDb ID {series_id}")

            return ByIMDb()
    else:
        logger.warning('Error connecting to EZTV API. The service may not be available at this time.')

        return ByIMDb()


def handle_request(api_url: str, parameters: dict) -> Any:
    try:
        request = requests.get(api_url, parameters)
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


def measure_number_pages(torrents_count: str) -> int:
    torrents_number = int(torrents_count)

    result = ceil(torrents_number / LIMIT)

    return result


def requests_remaining_pages(series_id: str, pages: int, torrents: List[dict]) -> List[dict]:
    result = torrents

    for page in range(INITIAL_PAGE + 1, pages + 1):
        payload = {'limit': LIMIT, 'page': page, 'imdb_id': series_id}
        request = handle_request(EZTV_API, payload)

        if (request is not None) and (request.status_code == 200):
            json_object = request.json()
            remaining_torrents = json_object['torrents']
            for remaining_torrent in remaining_torrents:
                result.append(remaining_torrent)
        else:
            logger.warning(f"Unable to retrieve page {page} of Torrents for the show with ID {series_id}")

    return result


def parse_available_torrents(torrents: List[dict]) -> List[TorrentAvailable]:
    result = []

    for torrent in torrents:
        filename = torrent['filename']
        torrent_url = torrent['torrent_url']
        magnet_url = torrent['magnet_url']
        title = torrent['title']
        season = torrent['season']
        episode = torrent['episode']
        seeds = torrent['seeds']
        peers = torrent['peers']
        size_bytes = torrent['size_bytes']
        size = int(size_bytes)

        torrent = TorrentAvailable(filename, torrent_url, magnet_url, title, season, episode, seeds, peers, size)
        result.append(torrent)

    return result
