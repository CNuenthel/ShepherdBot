""" Scraping tools to navigate and obtain document data from the Toyhou.se website """

import requests
from bs4 import BeautifulSoup
import random
from img.img_path import image_path


class ToyHouseScraper:
    """ Scraper tool to manage Toyhou.se documents """
    def __init__(self):
        self.route = None
        self.main_soup = None
        self.max_pages = 0
        self.image_count = 0

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

    def set_route(self, th_username: str):
        """ Sets standard route to Toyhou.se website user page all-character folder """
        self.route = f"https://toyhou.se/{th_username}/characters/folder:all"
        self._get_main_document()
        self._get_total_page_numbers()

    def _get_main_document(self):
        """ Get document from all folder Toyhou.se user page """
        self.main_soup = self.scrape_document(self.route)

    def _get_total_page_numbers(self):
        """ Get total page numbers within all folder """
        uls = self.main_soup.find("ul", {"class": "pagination paginator-center"})
        self.max_pages = int("".join([li.text for li in uls.find_all("li")][-2:-1]))

    def verify_user_found(self):
        """ Verify that a user page exists """
        if self.route:
            response = requests.get(self.route)
            if response.status_code == 200:
                return True
            else:
                return False
        raise ValueError("Route has not been set, set Toyhou.se page route with set_route method")

    def scrape_random_image(self) -> (str, str):
        """
        Returns a tuple containing a random image url and its corresponding text from Toyhou.se user all folder
        """
        random_soup = self.scrape_document(self.route + f"?page={random.randint(1, self.max_pages)}")

        thumbs = self.list_img_source(random_soup.find_all("a", {"class": "img-thumbnail"}))
        names = self.list_element_texts(random_soup.find_all("span", {"class": "thumb-character-name"}))

        img_url, img_caption = random.choice(tuple(zip(thumbs, names)))
        img_path = self.request_image(img_url)

        return [img_path, img_caption]

    def request_image(self, image_url: str) -> str:
        """ Scrapes and saves an image to file from url """
        result = requests.get(image_url)
        self.image_count += 1

        # If an image was scraped, save it to file and return its path
        if result.status_code == 200:
            with open(image_path+f"{self.image_count}.png", "wb") as f:
                f.write(result.content)
            return image_path+f"{self.image_count}.png"




