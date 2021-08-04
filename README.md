# Check episode or movie (Telegram bot)

![build](https://img.shields.io/badge/build-passing-brightgreen) ![license](https://img.shields.io/badge/license-MIT-brightgreen) ![python](https://img.shields.io/badge/python-3.8%2B-blue) ![platform](https://img.shields.io/badge/platform-linux--64%20%7C%20win--64-lightgrey)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MinionAttack_CheckEpisodeOrMovieBot&metric=alert_status)](https://sonarcloud.io/dashboard?id=MinionAttack_CheckEpisodeOrMovieBot)

Table of contents.

1. [Author disclaimer](#author-disclaimer)
2. [Introduction](#introduction)
3. [Requisites](#requisites)
4. [Project structure](#project-structure)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [How to use](#how-to-use)
8. [Special thanks](#special-thanks)
9. [Licensing agreement](#licensing-agreement)

## Author disclaimer

This project has been carried out solely and exclusively for self-learning reasons and to show it as a career portfolio.

This project does not violate the *Digital Millennium Copyright Act* (*DMCA*) because it only indicates where the information the user is
looking for is located. No software, images, movies, series or music are stored on a server owned by the author of this project and this bot
does not make illegal copies, or damage or infringe any *Copyright*©.

Everything that this bot processes and sends to the user who has requested it is available on the *World Wide Web*, the Internet, so this
bot only limits itself to saying where the information is and how to get it, this bot does not provide it.

## Introduction

Every week, when I want to check if a movie or the episodes of the series that I follow are already published, I have to visit some web
pages that I use to download the episodes and look at them one by one.

Although it doesn't take long, it doesn't stop being repetitive and it's always the same, so I thought... why do it myself when a bunch of
0's and 1's can do it for me and save me that time?

And that is why you are reading this.

## Requisites

In order to use the bot it is necessary to have a compatible environment:

- **Operative system**: A *Linux* or *Windows* based system where the bot will run.
- **Python version**: The bot has been developed with version *3.8.5*. It may work with older versions, but this has not been tested.
- **A Telegram account**: You need to have a *Telegram* account to be able to run the bot, configure the bot, access it and use it. You can
  create an account at the following [link][1].
- **An OMDb API account**: You need to have an *OMDb API* account to run the bot as it is the provider of *IMDb* identifiers for series and
  these identifiers are used to find *Torrent* files. With a *free account* it is enough if you are not going to have a high number of
  requests, since this account *is limited to 1000 requests per day*. You can create an account at the following [link][2]. **Remember to
  validate the *API Key* by clicking the activation link in the activation email sent after completing the registration process**.

[1]: https://web.telegram.org/#/login

[2]: http://www.omdbapi.com/apikey.aspx

## Project structure

In this section you can have a quick view of the project structure.

```
.
├── logs (*)
│   ├── critical.txt
│   ├── errors.txt
│   ├── info.txt
│   ├── warn.txt
│   └── debug.txt
├── LICENSE
├── README.md
├── requirements.txt
├── providers
│   ├── EZTV.py
│   ├── OMDbAPI.py
│   ├── YTS.py
│   └── YIFY.py
├── classes
│   ├── ConvertBytes.py
│   ├── EZTV.py
│   ├── YTS.py
│   ├── SeriesCommand.py
│   ├── OMDbAPI.py
│   ├── YIFY.py
│   ├── MoviesCommand.py
│   └── SubtitlesCommand.py
├── src
│   ├── bot.py
│   ├── logger.py
│   ├── command_handlers.py
│   └── utils.py
├── resources
│   ├── log.yaml
│   └── properties.py
├── strings
│   ├── command_handlers.py
│   ├── OMDbAPI.py
│   ├── movies_command.py
│   ├── series_command.py
│   ├── subtitles_command.py
│   └── help_command.py
└── actions
    ├── movies_command.py
    ├── series_command.py
    ├── subtitles_command.py
    └── help_command.py
```

Directories marked with a (*) will be created by the bot as needed.

## Installation

This section expects the requirements stated in the previous section to be met and this is how this section has been written.

- **Program dependencies**: The bot has some dependencies that must be installed in order to work. Those dependencies can be installed with
  the _requirements.txt_ file:
    - `pip install -r requirements.txt`
- It is highly recommended to use a **virtual environment** (*venv*), so the bot dependencies installation will not conflict with the
  packages installed on the system.

If you want to run the bot in a *venv*, open a terminal in the project's root folder and run:

```
source path_to_your_virtual_environment/bin/activate
pip install -r requirements.txt
```

If you do not want to run the bot in a *venv*, open a terminal in the project's root folder and run:

```
pip install -r requirements.txt
```

**Note**: If you have both **Python 2** and **Python 3** installed on your system, use **pip3** instead of **pip**.

## Configuration

There are some parameters that need to be set by the user, so the bot can work. Those parameters are in the */resources/properties.py* file.

- **BOT_TOKEN**: This is the authorization token given to you by [BotFather][3]. In the previous link you have all the information and the
  steps to generate a token and the rest of the commands to configure the details of the bot.
- **OMDB_API_KEY**: This is the API key that was sent to you in an email after completing the registration process. **It must have been
  activated in order to work**.

[3]: https://core.telegram.org/bots#6-botfather

There are other properties in the file, but they should not be changed unless you know what you are doing or if you want to continue with
the development of the bot.

## How to use

You can use the bot in two ways.

- Accessing the official instance of the bot running on my personal *Raspberry Pi 3B+* in my apartment by clicking on the following link:
    - [https://t.me/CheckEpisodeOrMovieBot][4]
    - There is no guarantee that it will be working 24/7.
- Using your own instance of the bot:
    - Remember to activate the *venv* if you are using it.
    - Add the root folder of the bot to *Python*'s path variable:
        - `export PYTHONPATH=$PYTHONPATH:/full/path/bot/root/folder/`
    - Go to the `src` folder of the project and grant execute permissions to `bot.py` file:
        - `$ chmod +x bot.py`
    - Start the bot:
        - `python3 bot.py`
    - To stop the bot just press `Control + C`.

Right now there are only six commands available:

- **Start**: Use this command to display the welcome message.
- **Status**: Use this command to find out if the bot is working. If you do not get a response from this command, the bot is not working.
- **Help**: Use this command to know how to use the bot. There are two types of syntax, one short and one long:
    - **Long syntax**: `/help -command command`
    - **Short syntax**: `/help -c command`
    - The available commands are: `start`, `status`, `help`, `series`, `movies`.
- **Series**: Use this command to search for available torrents for an episode of a series. There are two syntaxes, one short and one long:
    - **Long syntax**: `/series -name name -year number -season number -episode number -quality number`
    - **Short syntax**: `/series -n name -y number -s number -e number -q number`
    - **Considerations to take into account**:
        - The name of the series must be spelled the same way it is displayed on **IMDb**.
        - If no year is specified, the bot uses the current year. This parameter is necessary to avoid name collisions in tv shows with the
          same name as a movie, because the *OMDb API* will return the result of a movie in case there is a match and the year is not
          specified.
        - The available qualities are: 480 (SD), 720 (HD), 1080 (FHD) and 2160 (UHD).
        - The number specified for the quality must not include the scan type. If you want HD content write 720 but not 720i or 720p, the
          same for SD (480) content, Full HD (1080) content and Ultra HD (2160) content. **Do not include the letter**.
        - When searching for an episode, the bot prioritises results that are a complete season pack rather than the individual result. *
          This behaviour does not interfere when trying to search for a specific episode as opening the result link allows you to select the
          specific episode you are looking for*.
        - The details shown in each tv show may vary depending on the name of the video file. For the same episode of a series, the
          details may not match because the files do not have the same structure or not all the details have been included in the file name.
- **Movies**: Use this command to search for available torrents for a movie. There are two syntaxes, one short and one long:
    - **Long syntax**: `/movies -name name -year number -quality number`
    - **Short syntax**: `/movies -n name -y number -q number`
    - **Considerations to take into account**:
        - The name of the movie must be spelled the same way it is displayed on **IMDb**.
        - If no year is specified, the bot uses the current year. This parameter is necessary to avoid name collisions in movies with the
          same name as the series, because the *OMDb API* will return the result of a series in case there is a match and the year is not
          specified.
        - The available qualities are: 480 (SD), 720 (HD), 1080 (FHD) and 2160 (UHD).
        - The number specified for the quality must not include the scan type. If you want HD content write 720 but not 720i or 720p, the
          same for SD (480) content, Full HD (1080) content and Ultra HD (2160) content. **Do not include the letter**.
        - The details shown in each movie may vary depending on the information provided by the third party components.
- **Subtitles**: Use this command to find the subtitles for a specific movie. There are two types of syntax, one short and one long:
    - **Long syntax**: `/subtitles -movie name -year number -language language -limit number`
    - **Short syntax**: `/subtitles -m name -y number -la language -li number`
    - **Considerations to take into account**:
        - The name of the movie must be spelled the same way it is displayed on **IMDb**.
        - If no year is specified, the bot uses the current year. This parameter is necessary to avoid name collisions in movies with the
          same name as the series, because the *OMDb API* will return the result of a series in case there is a match and the year is not
          specified.
        - The available languages are: Albanian, Arabic, Armenian, Bengali, Bosnian, Brazilian Portuguese, Bulgarian, Burmese, Chinese,
          Croatian, Czech, Danish, Dutch, English, Estonian, Farsi/Persian (Same results), Finnish, French, German, Greek, Hebrew, Hindi,
          Hungarian, Icelandic, Indonesian, Italian, Japanese, Korean, Lithuanian, Macedonian, Malay, Malayalam, Nepali, Norwegian, Pashto,
          Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swedish, Tamil, Telugu, Thai, Turkish, Ukrainian,
          Urdu, Vietnamese.
        - The number specified for the limit indicates how many results will be displayed. **This parameter is optional**, by default the
          first 5 results with the highest score are shown.
        - **Be careful when specifying a limit**. Do this only if the default value is not enough to find a valid subtitle because in some
          movies there are languages with LOTS of options available (in some cases close to 80 possibilities), so specifying a higher limit
          could result in receiving a large number of very long messages.

[4]: https://t.me/CheckEpisodeOrMovieBot

## Special thanks

I want to especially thank my dear sister for helping me with the design and drawing of the bot logo. Without the help of my sister, the bot
would not have such a distinctive and cool logo.

## Licensing agreement

Copyright © 2020 MinionAttack

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "
Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the
following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
