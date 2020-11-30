# -*- coding: utf-8 -*-

from typing import List


class DisplayTorrentInformation:
    def __init__(self, torrent_url: str = '', quality: str = '', release_type: str = '', health: str = '', size: str = ''):
        self.torrent_url = torrent_url
        self.quality = quality
        self.release_type = release_type
        self.health = health
        self.size = size

    def __str__(self):
        return f"Torrent URL: {self.torrent_url}\nQuality: {self.quality}\nType: {self.release_type}\nHealth: {self.health}\n" \
               f"Size: {self.size}\n"


class DisplayMovieInformation:
    def __init__(self, title: str = '', year: int = 0, rating: str = '', runtime: str = '', genres: str = '', youtube_trailer: str = '',
                 mpa_rating: str = '', large_cover_image: str = '', torrents: List[DisplayTorrentInformation] = None):
        self.title = title
        self.year = year
        self.rating = rating
        self.runtime = runtime
        self.genres = genres
        self.youtube_trailer = youtube_trailer
        self.mpa_rating = mpa_rating
        self.large_cover_image = large_cover_image
        self.torrents = torrents

    def __str__(self):
        return f"Title: {self.title}\nYear: {self.year}\nRating: {self.rating}\nRuntime: {self.runtime}\n" \
               f"Genres: {self.genres}\nYouTube trailer: {self.youtube_trailer}\nMPA rating: {self.mpa_rating}\nCover image: " \
               f"{self.large_cover_image}\nTorrents: {self.torrents}\n"


class SendInformation:
    def __init__(self, photo_url: str = '', message: str = ''):
        self.photo_url = photo_url
        self.message = message

    def __str__(self):
        return f"Photo URL: {self.photo_url}\nMessage: {self.message}\n"


class Options:
    def __init__(self, movie_name: str = '', quality: str = ''):
        self.movie_name = movie_name
        self.quality = quality

    def __str__(self):
        return f"Movie name: {self.movie_name}\nQuality: {self.quality}\n"
