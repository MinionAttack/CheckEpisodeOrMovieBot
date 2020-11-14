# -*- coding: utf-8 -*-

from math import ceil
from typing import List

import requests

from classes.TorrentSearchResult import ByIMDb, TorrentAvailable
from src.logger import logger

EZTV_API = 'https://eztv.re/api/get-torrents?limit={}&page={}&imdb_id={}'
# Results per page, between 1 and 100
LIMIT = 100
INITIAL_PAGE = 1


def search_show_by_imdb(show_id: str) -> ByIMDb:
    request = requests.get(EZTV_API.format(LIMIT, INITIAL_PAGE, show_id))

    if request.status_code == 200:
        json_object = request.json()

        imdb_id = json_object['imdb_id']
        torrents_count = json_object['torrents_count']
        torrents = json_object['torrents']
        pages = measure_number_pages(torrents_count)
        if pages > 1:
            total_torrents = requests_remaining_pages(show_id, pages, torrents)
        else:
            total_torrents = torrents
        parsed_torrents = parse_available_torrents(total_torrents)
        result = ByIMDb(imdb_id, torrents_count, parsed_torrents)

        return result
    else:
        logger.warning(f"No results for the show with IMDb ID {show_id}")

        return ByIMDb()


def measure_number_pages(torrents_count: str) -> int:
    torrents_number = int(torrents_count)

    result = ceil(torrents_number / LIMIT)

    return result


def requests_remaining_pages(show_id: str, pages: int, torrents: List[dict]) -> List[dict]:
    result = torrents

    for page in range(INITIAL_PAGE + 1, pages + 1):
        request = requests.get(EZTV_API.format(LIMIT, page, show_id))

        if request.status_code == 200:
            json_object = request.json()
            remaining_torrents = json_object['torrents']
            for remaining_torrent in remaining_torrents:
                result.append(remaining_torrent)
        else:
            logger.warning(f"Unable to retrieve page {page} of Torrents for the show with ID {show_id}")

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
