import requests

from bs4 import BeautifulSoup


class DataLoader:

    def __init__(self, calendar_url: str) -> None:
        self.calendar_url = calendar_url