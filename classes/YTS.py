# -*- coding: utf-8 -*-

from typing import List


class TorrentAvailable:
    def __init__(self, torrent_url: str = '', quality: str = '', release_type: str = '', seeds: int = 0, peers: int = 0,
                 size_bytes: int = 0):
        self.torrent_url = torrent_url
        self.quality = quality
        self.release_type = release_type
        self.seeds = seeds
        self.peers = peers
        self.size_bytes = size_bytes

    def __str__(self):
        return f"Torrent URL: {self.torrent_url}\nQuality: {self.quality}\nType: {self.release_type}\nSeeds/Peers: {self.seeds}/" \
               f"{self.peers}\nSize (bytes): {self.size_bytes}\n"


class ByIMDb:
    def __init__(self, imdb_code: str = '', title: str = '', year: int = 0, rating: float = 0.0, runtime: int = 0, genres: str = '',
                 synopsis: str = '', youtube_trailer: str = '', language: str = '', mpa_rating: str = '', large_cover_image: str = '',
                 torrents: List[TorrentAvailable] = None):
        self.imdb_code = imdb_code
        self.title = title
        self.year = year
        self.rating = rating
        self.runtime = runtime
        self.genres = genres
        self.synopsis = synopsis
        self.youtube_trailer = youtube_trailer
        self.language = language
        self.mpa_rating = mpa_rating
        self.large_cover_image = large_cover_image
        self.torrents = torrents

    def __str__(self):
        return f"IMBd code: {self.imdb_code}\nTitle: {self.title}\nYear: {self.year}\nRating: {self.rating}\nRuntime: {self.runtime}\n" \
               f"Genres: {self.genres}\nSynopsis: {self.synopsis}\nYouTube trailer: {self.youtube_trailer}\nLanguage: {self.language}\n" \
               f"MPA rating: {self.mpa_rating}\nCover image: {self.large_cover_image}\nTorrents: {self.torrents}\n"

    def is_empty(self):
        return self.imdb_code == '' and self.title == '' and self.year == 0 and self.rating == 0 and self.runtime == 0 and \
               self.genres == '' and self.synopsis == '' and self.youtube_trailer == '' and self.language == '' and self.mpa_rating == '' \
               and self.large_cover_image == '' and self.torrents is None
