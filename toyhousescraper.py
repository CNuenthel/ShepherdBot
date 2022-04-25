""" Scraping tools to navigate and obtain document data from the Toyhou.se website """

import requests
from bs4 import BeautifulSoup
import random


class ToyHouseScraper:
    """ Scraper tool to manage Toyhou.se documents """
    def __init__(self, th_username: str):
        self.route = f"https://toyhou.se/{th_username}/characters/folder:all"

        """ Internal functions """
        self._get_main_document()
        self._get_total_page_numbers()

    @staticmethod
    def scrape_document(url: str):
        html = requests.get(url)
        return BeautifulSoup(html.text, "html.parser")

    @staticmethod
    def list_img_source(thumbs: list) -> list:
        """ Returns a list of source urls from document anchor elements """
        return [anchor.find("img")["src"] for anchor in thumbs]

    @staticmethod
    def list_element_texts(elements: list) -> list:
        """ Returns a list of texts housed by HTML elements """
        return [element.text for element in elements]

    def _get_main_document(self):
        """ Get document from all folder Toyhou.se user page """
        self.main_soup = self.scrape_document(self.route)

    def _get_total_page_numbers(self):
        """ Get total page numbers within all folder """
        uls = self.main_soup.find("ul", {"class": "pagination paginator-center"})
        self.max_pages = int("".join([li.text for li in uls.find_all("li")][-2:-1]))

    def scrape_random_image(self) -> (str, str):
        """
        Returns a tuple containing a random image url and its corresponding text from Toyhou.se user all folder
        """
        page_number = random.randint(1, self.max_pages)
        random_soup = self.scrape_document(f"https://toyhou.se/Flipside/characters/folder:all?page={page_number}")
        thumbs = self.list_img_source(random_soup.find_all("a", {"class": "img-thumbnail"}))
        names = self.list_element_texts(random_soup.find_all("span", {"class": "thumb-character-name"}))

        return random.choice(tuple(zip(thumbs, names)))

