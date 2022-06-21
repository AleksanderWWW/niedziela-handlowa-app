import typing
import logging

import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from backend import backend_exceptions


class DataLoader:

    def __init__(self, calendar_url: str) -> None:
        self.calendar_url = calendar_url

    def load_raw_data(self, year: typing.Union[int, str], 
                      force_on_error: bool = False) -> str:
        """
        Method performs GET request to the source web site and
        retrieves html content containing the dates of non-trade
        Sundays in a raw form.
        
        :param int or str year: year for which to retreive the data
        :param bool force_on_error: indicates whether to disable verification
        upon SSLError and retry

        :return: html content of the source website
        :rtype: str
        """
        # check for string year beginning with slash
        # that would mess with urljoin function
        if isinstance(year, str) and year[0] == "/":
            year = year[1:]

        try:
            int(year)
        except ValueError:
            raise backend_exceptions.InvalidInputParameters(f"Provided year {year} is invalid")

        url = urljoin(self.calendar_url, str(year))

        try:
            response = requests.get(url)
        except requests.exceptions.SSLError as e:
            logging.warning(e)
            if not force_on_error:
                logging.info("returning empty string since force_on_error=False")
                return ""
            
            logging.info("disabling certificate verification and retrying")
            response = requests.get(url, verify=False)

        return response.text
