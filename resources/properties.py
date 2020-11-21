# -*- coding: utf-8 -*-

BOT_TOKEN = ''

OMDB_API_KEY = ''

# DOT NOT MODIFY THE BELOW PROPERTIES UNLESS YOU ARE DEVELOPING THE BOT #

LOGS_FOLDER = 'logs'

LOGS_MODE = 'development'

AVAILABLE_HELP_COMMANDS = ['start', 'status', 'help', 'series', 'movies']

RESOLUTION_QUALITY = ['480p', '720p', '1080p', '2160p']

# https://en.wikipedia.org/wiki/Pirated_movie_release_types
PLATFORMS = {'ABC': 'American Broadcasting Company', 'ATVP': 'Apple TV +', 'AMZN': 'Amazon Studios',
             'BBC': 'British Broadcasting Corporation', 'BOOM': 'Boomerang', 'CBC': 'Canadian Broadcasting Corporation',
             'CBS': 'CBS Corporation', 'CC': 'Comedy Central', 'CR': 'Crunchyroll', 'CRAV': 'Crave',
             'CRITERION': 'The Criterion Collection', 'CW': 'The CW', 'DCU': 'DC Universe', 'DSNP': 'Disney Plus',
             'DSNY': 'Disney Networks', 'FBWatch': 'Facebook Watch', 'FREE': 'Freeform', 'FOX': 'Fox Broadcasting Company',
             'HMAX': 'HBO Max', 'HULU': 'Hulu Networks', 'iP': 'BBC iPlayer', 'iT': 'iTunes', 'LIFE': 'Lifetime', 'MTV': 'MTV Networks',
             'NBC': 'National Broadcasting Company', 'NICK': 'Nickelodeon', 'NF': 'Netflix', 'OAR': 'Original Aspect Ratio',
             'PCOK': 'Peacock', 'RED': 'YouTube Premium', 'TVNZ': 'TVNZ', 'STAN': 'Stan', 'STZ': 'STARZ'}

EXTRA_QUALITY_OPTIONS = ['HDR', '10bit', '12bit', 'Atmos']

HDTV_PDTV_DSRIP = ['DSR', 'DSRip', 'SATRip', 'DTHRip', 'DVBRip', 'HDTV', 'PDTV', 'DTVRip', 'TVRip', 'HDTVRip']

WEB_DL = ['WEBDL', 'WEB DL', 'WEB-DL', 'HDRip', 'WEB-DLRip']

WEBRIP = ['WEBRip', 'WEB Rip', 'WEB-Rip', 'WEB']

HC_HD_Rip = ['HC', 'HD-Rip']

BD_BDRIP = ['Blu-Ray', 'BluRay', 'BLURAY', 'BDRip', 'BRip', 'BRRip', 'BDMV', 'BDR', 'BD25', 'BD50', 'BD5', 'BD9']

IMAGE_FORMAT = {'HDTV_PDTV_DSRip': HDTV_PDTV_DSRIP, 'WEB_DL': WEB_DL, 'WEBRIP': WEBRIP, 'HC_HD_Rip': HC_HD_Rip, 'BD_BDRIP': BD_BDRIP}
