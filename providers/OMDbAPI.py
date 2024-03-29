# -*- coding: utf-8 -*-

from classes.OMDbAPI import MovieByName, SeriesByName
from resources.properties import OMDB_API_KEY
from src.logger import logger
from src.utils import handle_request
from strings.OMDbAPI import MOVIE_NOT_FOUND, OMDBAPI_ERROR_RESPONSE_MESSAGE, SERIES_NOT_FOUND

OMDB_API_URL = 'https://www.omdbapi.com/'


def search_series_by_name(name: str, year: int) -> SeriesByName:
    payload = {'apikey': OMDB_API_KEY, 't': name, 'y': year}
    request = handle_request(OMDB_API_URL, None, payload)

    if (request is not None) and (request.status_code == 200):
        json_object = request.json()
        response = json_object['Response']

        if response == 'True':
            content_type = json_object['Type']
            if content_type == 'series':
                result = get_series_data(json_object)
                return result
            else:
                return SeriesByName(content_type=content_type)
        else:
            error = json_object['Error']
            logger.warning(f"Error from OMDb API: {error}")
            if error == OMDBAPI_ERROR_RESPONSE_MESSAGE:
                return SeriesByName(error=True, error_message=SERIES_NOT_FOUND)
            else:
                return SeriesByName(error=True, error_message=error)
    else:
        logger.warning('Error connecting to OMDb API. The service may not be available at this time.')

        return SeriesByName()


def get_series_data(json_object: dict) -> SeriesByName:
    title = json_object['Title']
    poster_url = json_object['Poster']
    seasons = json_object['totalSeasons']
    imdb_id = json_object['imdbID']
    parsed_imdb_id = imdb_id[2:10]
    content_type = json_object['Type']

    result = SeriesByName(title, poster_url, seasons, imdb_id, parsed_imdb_id, content_type)

    return result


def search_movie_by_name(name: str, year: int) -> MovieByName:
    payload = {'apikey': OMDB_API_KEY, 't': name, 'y': year}
    request = handle_request(OMDB_API_URL, None, payload)

    if (request is not None) and (request.status_code == 200):
        json_object = request.json()
        response = json_object['Response']

        if response == 'True':
            content_type = json_object['Type']
            if content_type == 'movie':
                result = get_movie_data(json_object)
                return result
            else:
                return MovieByName(content_type=content_type)
        else:
            error = json_object['Error']
            logger.warning(f"Error from OMDb API: {error}")
            if error == OMDBAPI_ERROR_RESPONSE_MESSAGE:
                return MovieByName(error=True, error_message=MOVIE_NOT_FOUND)
            else:
                return MovieByName(error=True, error_message=error)
    else:
        logger.warning('Error connecting to OMDb API. The service may not be available at this time.')

        return MovieByName()


def get_movie_data(json_object: dict) -> MovieByName:
    title = json_object['Title']
    poster_url = json_object['Poster']
    imdb_id = json_object['imdbID']
    content_type = json_object['Type']

    result = MovieByName(title, poster_url, imdb_id, content_type)

    return result
