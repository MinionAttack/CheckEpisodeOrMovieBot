# -*- coding: utf-8 -*-

class SeriesByName:
    def __init__(self, title: str = '', poster_url: str = '', seasons: str = '', imdb_id: str = '', parsed_imdb_id: str = '',
                 content_type: str = '', error: bool = False, error_message: str = ''):
        self.title = title
        self.poster_url = poster_url
        self.seasons = seasons
        self.imdb_id = imdb_id
        self.parsed_imdb_id = parsed_imdb_id
        self.content_type = content_type
        self.error = error
        self.error_message = error_message

    def __str__(self):
        return f"Title: {self.title}\nPoster URL: {self.poster_url}\nSeasons: {self.seasons}\nIMDb ID: {self.imdb_id}\n" \
               f"Parsed IMDb ID: {self.parsed_imdb_id}\nContent type: {self.content_type}\nError message: {self.error_message}\n"

    def is_empty(self):
        return self.title == '' and self.poster_url == '' and self.seasons == '' and self.imdb_id == ''

    def is_series(self):
        return self.content_type == 'series'


class MovieByName:
    def __init__(self, title: str = '', poster_url: str = '', imdb_id: str = '', content_type: str = '', error: bool = False,
                 error_message: str = ''):
        self.title = title
        self.poster_url = poster_url
        self.imdb_id = imdb_id
        self.content_type = content_type
        self.error = error
        self.error_message = error_message

    def __str__(self):
        return f"Title: {self.title}\nPoster URL: {self.poster_url}\nIMDb ID: {self.imdb_id}\nContent type: {self.content_type}\n" \
               f"Error message: {self.error_message}\n"

    def is_empty(self):
        return self.title == '' and self.poster_url == '' and self.imdb_id == ''

    def is_movie(self):
        return self.content_type == 'movie'
