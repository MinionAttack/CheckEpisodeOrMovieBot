# -*- coding: utf-8 -*-

class ByName:
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

    def is_tv_show(self):
        return self.content_type == 'series'
