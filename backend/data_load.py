import os
import typing
import logging


import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

from urllib.parse import urljoin

from backend import backend_exceptions


class DataLoader:

    def __init__(self, calendar_url: str) -> None:
        self.calendar_url = calendar_url
        self.sundays_file_template = "sundays_{year}.txt"

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

        # handle a case where data for the chosen year had already been loaded
        if os.path.isfile(self.sundays_file_template.format(year=year)):
            logging.info("Loading already present content")
            with open(self.sundays_file_template.format(year=year), "r", encoding="utf-8") as fp:
                return fp.read()

        url = urljoin(self.calendar_url, str(year))

        try:
            response = requests.get(url)
        except requests.exceptions.SSLError as e:
            logging.warning(e)
            if not force_on_error:
                logging.info("returning empty string since force_on_error=False")
                return ""
            
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            logging.info("disabling certificate verification and retrying")
            response = requests.get(url, verify=False)

        # save content to a file
        with open(self.sundays_file_template.format(year=year), "w", encoding="utf-8") as fp:
            fp.write(response.text)

        return response.text
