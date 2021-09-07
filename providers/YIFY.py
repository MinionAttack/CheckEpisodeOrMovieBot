# -*- coding: utf-8 -*-

from typing import List

from lxml.cssselect import CSSSelector
from lxml.html import fromstring, HtmlElement

from classes.YIFY import ByIMDb
from resources.properties import BROWSER_USER_AGENT
from src.logger import logger
from src.utils import handle_request

YIFY_API = 'https://yifysubtitles.org/movie-imdb/'
YIFY_DOWNLOAD = 'https://yifysubtitles.org/subtitle/'
YIFY_DOWNLOAD_EXTENSION = '.zip'

RATING_CSS_CLASS = 'rating-cell'
FLAG_CSS_CLASS = 'flag-cell'
LANGUAGE_CSS_CLASS = 'sub-lang'
SUBTITLE_CSS_CLASS = 'text-muted'
UPLOADER_CSS_CLASS = 'uploader-cell'


def search_subtitles_by_imdb(movie_id: str, language: str) -> List[ByIMDb]:
    movie_url = YIFY_API + movie_id
    # The User-Agent has to be specified to avoid the "requests.exceptions.TooManyRedirects" exception.
    headers = {'User-Agent': BROWSER_USER_AGENT, 'Upgrade-Insecure-Requests': '1', 'DNT': '1'}
    request = handle_request(movie_url, headers, None)

    if (request is not None) and (request.status_code == 200):
        content = request.text
        language_rows = find_language_rows(content, language)
        if language_rows:
            available_subtitles = get_subtitles_details(language_rows)
            return available_subtitles
        else:
            return []
    else:
        logger.warning('Error connecting to YIFY API. The service may not be available at this time.')
        return []


def find_language_rows(content: str, language: str):
    html_content = fromstring(content)
    language_selector = CSSSelector(f"span.{LANGUAGE_CSS_CLASS}")
    language_cells = language_selector(html_content)

    rows = []
    for cell in language_cells:
        language_text = cell.text_content().lower()
        if "/" not in language_text:
            if language == language_text:
                row = cell.getparent().getparent()
                rows.append(row)
        else:
            if language in language_text:
                row = cell.getparent().getparent()
                rows.append(row)

    return rows


# https://www.w3schools.com/cssref/css_selectors.asp
def get_subtitles_details(rows: List[HtmlElement]) -> List[ByIMDb]:
    rating_selector = CSSSelector(f"td.{RATING_CSS_CLASS} span.label")
    language_selector = CSSSelector(f"td.{FLAG_CSS_CLASS} span.{LANGUAGE_CSS_CLASS}")
    subtitle_selector = CSSSelector(f"a span.{SUBTITLE_CSS_CLASS}")
    uploader_selector = CSSSelector(f"td.{UPLOADER_CSS_CLASS}")

    subtitles = []
    for row in rows:
        rating = process_rating_cell(row, rating_selector)
        language = process_language_cell(row, language_selector)
        compatible_torrents, download_link = process_compatible_torrents_cell(row, subtitle_selector)
        uploader = process_uploader_cell(row, uploader_selector)

        subtitle = ByIMDb(rating, language, compatible_torrents, uploader, download_link)
        subtitles.append(subtitle)

    # https://stackoverflow.com/a/48731059/3522933, https://portingguide.readthedocs.io/en/latest/comparisons.html#rich-comparisons
    sorted_by_rating = sorted(subtitles, reverse=True)

    return sorted_by_rating


def process_rating_cell(row: HtmlElement, selector: CSSSelector) -> int:
    rating = 0

    elements = selector(row)
    if len(elements) == 1:
        rating = elements[0].text_content()
        if is_a_number(rating):
            rating = int(rating)
        else:
            logger.warning('The structure of the table has changed. The score value is not a number.')
    else:
        logger.warning('The structure of the table has changed. There is more than one score value.')

    return int(rating)


def is_a_number(number: str) -> bool:
    try:
        int(number)
        return True
    except ValueError:
        return False


def process_language_cell(row: HtmlElement, selector: CSSSelector) -> str:
    language = ''

    elements = selector(row)
    if len(elements) == 1:
        language = elements[0].text_content()
    else:
        logger.warning('The structure of the table has changed. There is more than one <span> tag in the language cell.')

    return language


def process_compatible_torrents_cell(row: HtmlElement, selector: CSSSelector) -> tuple:
    download_link = ''
    subtitles = ''

    elements = selector(row)
    if len(elements) == 1:
        link_element = elements[0].getparent()
        redirection_path = link_element.get('href')
        download_link = get_download_link(redirection_path)
        content = link_element.text_content()
        subtitles = content.split('subtitle ')[1]
    else:
        logger.warning('The structure of the table has changed. There is more than one <a> tag in the subtitle name cell.')

    return subtitles, download_link


def get_download_link(redirection_path: str) -> str:
    cleaned_redirection_path = redirection_path.replace('/subtitles/', '')
    download_link = YIFY_DOWNLOAD + cleaned_redirection_path + YIFY_DOWNLOAD_EXTENSION

    return download_link


def process_uploader_cell(row: HtmlElement, selector: CSSSelector) -> str:
    uploader = ''

    elements = selector(row)
    if len(elements) == 1:
        uploader = elements[0].text_content()
    else:
        logger.warning('The structure of the table has changed. There is more than one uploader value.')

    return uploader
