# -*- coding: utf-8 -*-

from typing import List


class Options:
    def __init__(self, movie: str = '', language_code: str = '', language: str = '', limit: int = 0):
        self.movie = movie
        self.language_code = language_code
        self.language = language
        self.limit = limit

    def __str__(self):
        return f"Movie: {self.movie}\nLanguage code: {self.language_code}\nLanguage: {self.language}\nLimit: {self.limit}\n"


class SendInformation:
    def __init__(self, photo_url: str = '', message: str = '', remaining_messages: List[str] = None):
        self.photo_url = photo_url
        self.message = message
        self.remaining_messages = remaining_messages

    def __str__(self):
        return f"Photo URL: {self.photo_url}\nMessage: {self.message}\nRemaining messages: {self.remaining_messages}\n"


class DisplaySubtitleInformation:
    def __init__(self, rating: str = '', language: str = '', compatible_torrents: str = '', uploader: str = '', download_link: str = ''):
        self.rating = rating
        self.language = language
        self.compatible_torrents = compatible_torrents
        self.uploader = uploader
        self.download_link = download_link

    def __str__(self):
        return f"Rating: {self.rating}\nLanguage: {self.language}\nCompatible torrents: {self.compatible_torrents}\nUploader: " \
               f"{self.uploader}\nDownload link: {self.download_link}\n"