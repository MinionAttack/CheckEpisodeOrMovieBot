# -*- coding: utf-8 -*-


class ByIMDb:
    def __init__(self, rating: int = 0, language: str = '', compatible_torrents: str = '', uploader: str = '', download_link: str = ''):
        self.rating = rating
        self.language = language
        self.compatible_torrents = compatible_torrents
        self.uploader = uploader
        self.download_link = download_link

    def __str__(self):
        return f"Rating: {self.rating}\nLanguage: {self.language}\nCompatible torrents: {self.compatible_torrents}\nUploader: " \
               f"{self.uploader}\nDownload link: {self.download_link}\n"

    def __eq__(self, other):
        return ((self.rating, self.language, self.compatible_torrents, self.uploader, self.download_link) ==
                (other.rating, other.language, other.compatible_torrents, other.uploader, other.download_link))

    def __ne__(self, other):
        return ((self.rating, self.language, self.compatible_torrents, self.uploader, self.download_link) !=
                (other.rating, other.language, other.compatible_torrents, other.uploader, other.download_link))

    def __lt__(self, other):
        return self.rating < other.rating

    def __le__(self, other):
        return self.rating <= other.rating

    def __gt__(self, other):
        return self.rating > other.rating

    def __ge__(self, other):
        return self.rating >= other.rating
