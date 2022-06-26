from datetime import date
from typing import List, Tuple

from .data_load import DataLoader
from .data_parse import DataParser


class Backend:
    """Class serving as a high-level orchestrator of lower-level
    data-flow-connected activities in the application"""
    def __init__(self, 
                 calendar_url: str) -> None:
        
        self.loader = DataLoader(calendar_url)
        self.parser = DataParser("")

        self.dates: List[Tuple[int]] = []

    def load_data(self, year: int, force_on_error: bool) -> None:
        """Scrapes and loads data into parser"""
        text = self.loader.load_raw_data(year, force_on_error=force_on_error)
        self.parser.set_page_source(text)

    def extract_dates(self) -> None:
        raw_dates = self.parser.find_raw_dates()

        for raw_date in raw_dates:
            self.dates.append(self.parser.parse_raw_date(raw_date))

    def check_if_date_work_free(self, day: int, month: int, year: int) -> bool:
        """For a given integer representstion of a date check if
        the date is work-free"""
        if date(year, month, day).weekday() != 6:
            return False

        for date_tuple in self.dates:
            if date_tuple[0] == day and date_tuple[1] == month:
                return False
        
        return True
