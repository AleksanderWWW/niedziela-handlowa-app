"""
Main runable application module. Run directly by:
 <path to python3 interpreter> app.py
 """

import json
import logging

from backend import Backend
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

    backend_interface = Backend(cal_url)
    app = web_app.WebApp(backend_interface)
    app.run()


if __name__ == "__main__":
    main()
