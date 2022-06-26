"""
Main runable application module. Run directly by:
 <path to python3 interpreter> app.py
 """

import json
import logging

from backend import data_load, data_parse
from frontend import web_app


def main():
    """
    Main runable function of the module
    """

    # read configuration file
    with open("config.json", "r", encoding="utf-8") as config_fp:
        config = json.load(config_fp)

    # configure logging
    fmt = config["general"]["logging_fmt"]
    logging.basicConfig(format=fmt, level=logging.INFO)
    
    # instantiate data loader
    cal_url = config["backend"]["calendar_url"]

    loader = data_load.DataLoader(cal_url)

    text = loader.load_raw_data(2021, force_on_error=True)

    parser = data_parse.DataParser(text)

    dates_raw = parser.find_raw_dates()
    dates = []
    for raw_date in dates_raw:
        dates.append(parser.parse_raw_date(raw_date))

    print(dates)

    app = web_app.WebApp(loader, parser)
    app.run()


if __name__ == "__main__":
    main()
