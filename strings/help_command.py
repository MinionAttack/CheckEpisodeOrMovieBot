# -*- coding: utf-8 -*-

INCORRECT_HELP_FORMAT = 'Incorrect format, see the /help command for more details. \U0001F635'

START_COMMAND_TEXT = 'Use this command to see the welcome message. \U0001F44B'

STATUS_COMMAND_TEXT = 'Use this command to check if the bot is up and running. <strong>If you do not get a response from this command, ' \
                      'the bot is not working</strong>. \U0001F6A5'

HELP_COMMAND_TEXT = 'Use this command to know how to use the bot. There are two types of syntax, one short and one long.\n\nTo use the ' \
                    'long syntax you must write:\n/help -command command\n\nTo use the short syntax you must write:\n/help -c command\n' \
                    '\n<strong>Available commands:</strong>\n\n1. start\n2. status\n3. help\n4. series\n5. movies\n6. subtitles'

SERIES_COMMAND_TEXT = 'Use this command to find a specific episode of a series. There are two types of syntax, one short and one long.' \
                      '\n\nTo use the long syntax you must write:\n/series -name name -season number -episode number -quality number\n\n' \
                      'To use the short syntax you must write:\n/series -n name -s number -e number -q number\n\n<strong>Important ' \
                      'notes:</strong>\n\n1. The name of the series must be spelled the same way it is displayed on <strong>IMDb' \
                      '</strong>.\n2. The available qualities are: 480 (SD), 720 (HD), 1080 (FHD) and 2160 (UHD).\n3. The number ' \
                      'specified for the quality must not include the scan type. If you want HD content write 720 but not 720i or 720p, ' \
                      'the same for SD (480) content, Full HD (1080) content and Ultra HD (2160) content. <strong>Do not include the ' \
                      'letter</strong>.'

MOVIES_COMMAND_TEXT = 'Use this command to find a specific movie. There are two types of syntax, one short and one long.\n\nTo use the ' \
                      'long syntax you must write:\n/movies -name name -year number -quality number\n\nTo use the short syntax you must ' \
                      'write:\n/movies -n name -y number -q number\n\n<strong>Important notes:</strong>\n\n1. The name of the movie must be ' \
                      'spelled the same way it is displayed on <strong>IMDb</strong>.\n2. If no year is specified, the bot uses the ' \
                      'current year. This parameter is necessary to avoid name collisions in movies with the same name as the series.\n' \
                      '3. The available qualities are: 480 (SD), 720 (HD), 1080 (FHD) and 2160 (UHD).\n3. The number specified for the ' \
                      'quality must not include the scan type. If you want HD content write 720 but not 720i or 720p, the same for SD ' \
                      '(480) content, Full HD (1080) content and Ultra HD (2160) content. <strong>Do not include the letter</strong>.'

SUBTITLES_COMMAND_TEXT = 'Use this command to find the subtitles for a specific movie. There are two types of syntax, one short and one ' \
                         'long.\n\nTo use the long syntax you must write:\n/subtitles -movie name -language language -limit number\n\n' \
                         'To use the short syntax you must write:\n/subtitles -m name -la language -li number\n\n<strong>Important notes' \
                         ':</strong>\n\n1. The name of the movie must be spelled the same way it is displayed on <strong>IMDb</strong>.' \
                         '\n2. If no year is specified, the bot uses the current year. This parameter is necessary to avoid name ' \
                         'collisions in movies with the same name as the series.\n3.The available languages are:\n\nAlbanian\nArabic\n' \
                         'Armenian\nBengali\nBosnian\nBrazilian Portuguese\nBulgarian\nBurmese\nChinese\nCroatian\nCzech\nDanish\nDutch\n' \
                         'English\nEstonian\nFarsi/Persian (Same results)\nFinnish\nFrench\nGerman\nGreek\nHebrew\nHindi\nHungarian\n' \
                         'Icelandic\nIndonesian\nItalian\nJapanese\nKorean\nLithuanian\nMacedonian\nMalay\nMalayalam\nNepali\nNorwegian\n' \
                         'Pashto\nPolish\nPortuguese\nRomanian\nRussian\nSerbian\nSlovak\nSlovenian\nSpanish\nSwedish\nTamil\nTelugu\n' \
                         'Thai\nTurkish\nUkrainian\nUrdu\nVietnamese\n\n4.The number specified for the limit indicates how many results ' \
                         'will be displayed. This parameter is optional, by default the first 5 results with the highest score are shown.' \
                         '\n5. <strong>Be careful when specifying a limit</strong>. Do this only if the default value is not enough to ' \
                         'find a valid subtitle because in some movies there are languages with LOTS of options available (in some cases ' \
                         'close to 80 possibilities), so <strong>specifying a higher limit could result in receiving a large number of ' \
                         'very long messages</strong>, like this one.'
