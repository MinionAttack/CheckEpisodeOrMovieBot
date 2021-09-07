# -*- coding: utf-8 -*-

from math import ceil
from typing import List

from classes.YTS import ByIMDb, TorrentAvailable
from resources.properties import BROWSER_USER_AGENT
from src.logger import logger
from src.utils import handle_request

# Use a proxy to evade ISP's blocking policies.
YTS_API = 'https://yts.torrentbay.to/api/v2/list_movies.json?'
# Results per page, between 1 and 50, default is 20.
LIMIT = 50
INITIAL_PAGE = 1

YOUTUBE_URL = 'https://www.youtube.com/watch?v='


def search_movie_by_imdb(movie_id: str, quality_specified: str) -> ByIMDb:
    # The User-Agent has to be specified to avoid Http Error: 403 Client Error
    headers = {'User-Agent': BROWSER_USER_AGENT, 'Upgrade-Insecure-Requests': '1', 'DNT': '1'}
    payload = {'limit': LIMIT, 'page': INITIAL_PAGE, 'query_term': movie_id}

    request = handle_request(YTS_API, headers, payload)

    if (request is not None) and (request.status_code == 200):
        json_object = request.json()
        status = json_object['status']
        status_message = json_object['status_message']

        if status == 'ok':
            data = json_object['data']
            movie_count = data['movie_count']
            if movie_count > 0:
                movies_available = data['movies']
                pages = measure_number_pages(movie_count)

                if pages > 1:
                    total_movies = requests_remaining_pages(movie_id, pages, movies_available)
                else:
                    total_movies = movies_available

                parsed_movies = parse_available_movies(total_movies, quality_specified)

                if parsed_movies.torrents:
                    return parsed_movies
                else:
                    return ByIMDb()
            else:
                return ByIMDb()
        elif status == 'error':
            logger.warning(f"The YTS API has returned an error for movie with IMDb ID {movie_id}: {status_message}")
            return ByIMDb()
    else:
        logger.warning(f"Error connecting to YTS API. The service may not be available at this time.")
        return ByIMDb()


def measure_number_pages(movie_count: str) -> int:
    torrents_number = int(movie_count)

    result = ceil(torrents_number / LIMIT)

    return result


def requests_remaining_pages(movie_id: str, pages: int, movies: List[dict]) -> List[dict]:
    result = movies

    for page in range(INITIAL_PAGE + 1, pages + 1):
        # The User-Agent has to be specified to avoid Http Error: 403 Client Error
        headers = {'User-Agent': BROWSER_USER_AGENT}
        payload = {'limit': LIMIT, 'page': page, 'query_term': movie_id}
        request = handle_request(YTS_API, headers, payload)

        if (request is not None) and (request.status_code == 200):
            json_object = request.json()
            status = json_object['status']
            status_message = json_object['status_message']

            if status == 'ok':
                data = json_object['data']
                remaining_movies = data['movies']
                for remaining_movie in remaining_movies:
                    result.append(remaining_movie)
            elif status == 'error':
                logger.warning(f"The YTS API has returned an error fetching the page {page} for the movie with IMDb ID {movie_id}: "
                               f"{status_message}")
        else:
            logger.warning(f"Unable to retrieve page {page} of available movies for the movie with IMDb ID {movie_id}")

        return result


def parse_available_movies(movies: List[dict], quality_specified) -> ByIMDb:
    # This should return a list of movies, but because I am using the IMDb ID to match the exact movie,
    # there will only be one item in the list.

    if len(movies) == 1:
        result = ByIMDb()

        for movie in movies:
            imdb_code = movie['imdb_code']
            title = movie['title']
            year = movie['year']
            rating = movie['rating']
            runtime = movie['runtime']
            raw_genres = movie['genres']
            genres = parse_genre(raw_genres)
            synopsis = movie['synopsis']
            youtube_trailer_code = movie['yt_trailer_code']
            youtube_trailer = create_youtube_trailer_link(youtube_trailer_code)
            language = movie['language']
            mpa_rating = movie['mpa_rating']
            proxy_cover_image = movie['large_cover_image']
            large_cover_image = get_cover_image_url(proxy_cover_image)
            raw_torrents = movie['torrents']
            torrents = parse_torrents(raw_torrents, quality_specified)

            option = ByIMDb(imdb_code, title, year, rating, runtime, genres, synopsis, youtube_trailer, language, mpa_rating,
                            large_cover_image, torrents)
            result = option

        return result
    else:
        return ByIMDb()


def parse_genre(genres: List[str]) -> str:
    result = ''

    for genre in genres:
        result = result + f"{genre}/"

    # Delete / at the end
    result = result[:-1]

    return result


def create_youtube_trailer_link(trailer_code: str) -> str:
    return YOUTUBE_URL + trailer_code


def get_cover_image_url(proxy_cover_image: str) -> str:
    # The User-Agent has to be specified to avoid Http Error: 403 Client Error
    headers = {'User-Agent': BROWSER_USER_AGENT}
    request = handle_request(proxy_cover_image, headers, None)
    url = request.url

    return url


def parse_torrents(torrents: List, quality_specified: str) -> List[TorrentAvailable]:
    result = []

    for torrent in torrents:
        quality = torrent['quality']
        if quality != quality_specified:
            continue
        else:
            torrent_url = torrent['url']
            release_type = torrent['type']
            seeds = torrent['seeds']
            peers = torrent['peers']
            size_bytes = torrent['size_bytes']

            option = TorrentAvailable(torrent_url, quality, release_type, seeds, peers, size_bytes)
            result.append(option)

    return result
