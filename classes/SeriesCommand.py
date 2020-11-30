# -*- coding: utf-8 -*-

from typing import List


class DisplayTorrentInformation:
    def __init__(self, title: str = '', season: str = '', episode: str = '', quality: str = '', platform: str = '', release_type: str = '',
                 subtitles: bool = False, file_type: str = '', size: str = '', scene: str = '', health: str = '', magnet_url: str = '',
                 torrent_url: str = ''):
        self.title = title
        self.season = season
        self.episode = episode
        self.quality = quality
        self.platform = platform
        self.release_type = release_type
        self.subtitles = subtitles
        self.file_type = file_type
        self.size = size
        self.scene = scene
        self.health = health
        self.magnet_url = magnet_url
        self.torrent_url = torrent_url

    def __str__(self):
        return f"Title: {self.title}\nSeason: {self.season}\nEpisode: {self.episode}\nQuality: {self.quality}\nPlatform: {self.platform}\n" \
               f"Release type: {self.release_type}\nSubtitles: {self.subtitles}\nFile type: {self.file_type}\nSize: {self.size}\n" \
               f"Scene: {self.scene}\nHealth: {self.health}\nMagnet URL: {self.magnet_url}\nTorrent URL: {self.torrent_url}\n"


class TemplateInformation:
    def __init__(self, poster_url: str = '', torrents: List[DisplayTorrentInformation] = None):
        self.poster_url = poster_url
        self.torrents = torrents

    def __str__(self):
        return f"Poster URL: {self.poster_url}\nTorrents: {self.torrents}\n"

    def is_empty(self):
        return self.poster_url == '' and self.torrents is None


class SendInformation:
    def __init__(self, photo_url: str = '', message: str = ''):
        self.photo_url = photo_url
        self.message = message

    def __str__(self):
        return f"Photo URL: {self.photo_url}\nMessage: {self.message}\n"


class Options:
    def __init__(self, series_name: str = '', season: str = '', episode: str = '', quality: str = ''):
        self.series_name = series_name
        self.season = season
        self.episode = episode
        self.quality = quality

    def __str__(self):
        return f"Series name: {self.series_name}\nSeason: {self.season}\nEpisode: {self.episode}\nQuality: {self.quality}\n"
