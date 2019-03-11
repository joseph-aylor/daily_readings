"""
Module daily readings is for pulling down the
daily mass readings
"""
import os
import requests
import pydoc
from datetime import date
from bs4 import BeautifulSoup
from pathlib import Path, PurePath


class Reading:
    FORMATTED_DATE = date.today().strftime('%m%d%y')

    def __init__(self, directory='daily_readings', date=date.today(), base_url='http://usccb.org/bible/readings/', url_extension='.cfm'):
        self.date = date
        self.directory_path = PurePath(Path.home(), directory)
        self.directory = Path(self.directory_path)
        self.file_path = PurePath(self.directory, f'{date}.txt')
        self.file = Path(self.file_path)
        self.url = f'{base_url}{self.formatted_date()}{url_extension}'

        self.ensuredirectoryexists()

    def ensuredirectoryexists(self):
        if not self.directory.is_dir():
            self.directory.mkdir()

    def formatted_date(self):
        return self.date.strftime('%m%d%y')

    def fetch(self, separator='============='):
        reading = ''
        HTML_STRING = requests.get(self.url).text
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

        self.reading = reading

    def has_file(self):
        return self.file.is_file()

    def save(self):
        self.file.write_text(self.reading)

    def open(self):
        if not self.has_file():
            self.fetch()
            self.save()

        self.reading = self.file.read_text()

    def growcache(self):
        pass

    def read(self):
        self.open()
        pydoc.pager(self.reading)
