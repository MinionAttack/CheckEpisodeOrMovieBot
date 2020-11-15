# -*- coding: utf-8 -*-

import requests

from classes.ShowSearchResult import ByName
from resources.properties import OMDB_API_KEY
from src.logger import logger

# http://www.omdbapi.com/?apikey=1343faf&i=tt3896198
# http://www.omdbapi.com/?apikey=1343faf&t=the+mandalorian
OMDB_API_URL = 'http://www.omdbapi.com/?apikey={}&t={}'


def search_show_by_name(name: str) -> ByName:
    request = requests.get(OMDB_API_URL.format(OMDB_API_KEY, name))

    if request.status_code == 200:
        json_object = request.json()
        response = json_object['Response']
        content_type = json_object['Type']

        if response == 'True' and content_type == 'series':
            title = json_object['Title']
            poster_url = json_object['Poster']
            seasons = json_object['totalSeasons']
            imdb_id = json_object['imdbID']
            parsed_imdb_id = imdb_id[2:10]
            result = ByName(title, poster_url, seasons, imdb_id, parsed_imdb_id, content_type)

            return result
        else:
            return ByName(content_type=content_type)
    else:
        logger.warning(f"Error connecting to OMDb API. The service may not be available at this time.")

        return ByName()
