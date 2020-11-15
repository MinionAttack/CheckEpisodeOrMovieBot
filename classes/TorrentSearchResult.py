# -*- coding: utf-8 -*-
from typing import List


class TorrentAvailable:
    def __init__(self, filename: str = '', torrent_url: str = '', magnet_url: str = '', title: str = '', season: str = '',
                 episode: str = '', seeds: int = 0, peers: int = 0, bytes_size: int = 0):
        self.filename = filename
        self.torrent_url = torrent_url
        self.magnet_url = magnet_url
        self.title = title
        self.season = season
        self.episode = episode
        self.seeds = seeds
        self.peers = peers
        self.bytes_size = int(bytes_size)

    def __str__(self):
        return f"File name: {self.filename}\nTorrent URL: {self.torrent_url}\nMagnet URL: {self.magnet_url}\nTitle: {self.title}\n" \
               f"Season: {self.season}\nEpisode: {self.episode}\nSeeds/Peers: {self.seeds}/{self.peers}\nSize (bytes): {self.bytes_size}\n"


class ByIMDb:
    def __init__(self, imdb_id: str = '', torrents_count: str = '', torrents: List[TorrentAvailable] = None):
        self.imdb_id = imdb_id
        self.torrents_count = torrents_count
        self.torrents = torrents

    def __str__(self):
        return f"IMDb ID: {self.imdb_id}\nNumber of torrents: {self.torrents_count}\nTorrents: {self.torrents}\n"

    def is_empty(self):
        return self.imdb_id == '' and self.torrents_count == '' and self.torrents is None
