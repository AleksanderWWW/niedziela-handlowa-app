import typing

from bs4 import BeautifulSoup


class DataParser:
    _DATE_STR_MAPPING = {
        "st": 1,
        "lu": 2,
        "ma": 3,
        "kw": 4,
        "ma": 5,
        "cz": 6,
        "li": 7,
        "si": 8,
        "wr": 9,
        "pa" : 10,
        "li": 11,
        "gr": 12
    }

    def __init__(self, page_source: str, html_parser: str = "lxml") -> None:
        self.page_source = page_source
        self.html_parser = html_parser
        self.soup = BeautifulSoup(page_source, html_parser)


    def find_raw_dates(self) -> typing.List[str]:
        """
        Parse the html page source and look for li elements
        containing raw representation of dates
        """
        main_section = self.soup.find("div", {"class": "left-column"})
        dates_ul = main_section.find("ul")
        dates = [date.text for date in dates_ul.find_all("li")]

        return dates

    def parse_raw_date(self, raw_date: str) -> typing.Tuple[int, int]:
        """
        Method takes raw string date representation as e.g. '30 stycznia'
        and turns it to a tuple of integers representing the day and 
        month respectively - tuple(30, 1) in this example.

        :param str raw_date: raw string represantation of a date
        """

        day_str, month_str = raw_date.split(" ")
        day_int = int(day_str)

        month_int = self._DATE_STR_MAPPING[month_str[:2]]

        return day_int, month_int
