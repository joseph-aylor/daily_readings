"""
Module daily readings is for pulling down the
daily mass readings
"""
import os
from datetime import date
import requests
from bs4 import BeautifulSoup
from pathlib import Path, PurePath

BASE_URL = 'http://usccb.org/bible/readings/'
URL_EXTENSION = '.cfm'
FORMATTED_DATE = date.today().strftime('%m%d%y')


def fetch(date=date.today(), separator='============='):
    reading = ''
    URL = '{base_url}{formatted_date}{url_extension}'.format(
        base_url=BASE_URL,
        formatted_date=FORMATTED_DATE,
        url_extension=URL_EXTENSION)
    HTML_STRING = requests.get(URL).text
    SOUP = BeautifulSoup(HTML_STRING, 'html.parser')
    for reading_tag in SOUP.find_all('div', {"class": "bibleReadingsWrapper"}):
        passage_id_tag = reading_tag.find('h4').find('a')
        if passage_id_tag:
            PASSAGE_ID = reading_tag.find('h4').find('a').text.replace(os.linesep, '')
            for e in reading_tag.find('div', {"class": "poetry"}).find_all("br"):
                e.replace_with(os.linesep)
            reading += separator
            reading += os.linesep
            reading += PASSAGE_ID
            reading += os.linesep
            reading += separator
            reading += os.linesep
            reading += reading_tag.find('div', {"class": "poetry"}).text

    return reading


def save(date=date.today(), directory='daily_readings'):
    file_name = PurePath(Path.home(), directory, f'{date}.txt')
    reading = fetch()
    print(file_name)

save()
