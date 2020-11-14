# -*- coding: utf-8 -*-

class ByName:
    def __init__(self, title: str = '', poster_url: str = '', seasons: str = '', imdb_id: str = '', parsed_imdb_id: str = ''):
        self.title = title
        self.poster_url = poster_url
        self.seasons = seasons
        self.imdb_id = imdb_id
        self.parsed_imdb_id = parsed_imdb_id

    def __str__(self):
        return f"Title: {self.title}\nPoster URL: {self.poster_url}\nSeasons: {self.seasons}\nIMDb ID: {self.imdb_id}\n" \
               f"Parsed IMDb ID: {self.parsed_imdb_id}\n"
