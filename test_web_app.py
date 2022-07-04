import json
import unittest
from app import main

from frontend.web_app import WebApp
from backend import Backend


class WebAppIndexTest(unittest.TestCase):
    with open("config.json", "r", encoding="utf-8") as CONFIG_FP:
        CONFIG = json.load(CONFIG_FP)

    CAL_URL = CONFIG["backend"]["calendar_url"]

    BACKEND_INTERFACE = Backend(CAL_URL)
    WEB_APP = WebApp(BACKEND_INTERFACE)

    def test_index_returns_200_status_code(self):
        tester = self.WEB_APP.app.test_client()
        response = tester.get("/")
        code = response.status_code
        
        self.assertEqual(code, 200)

    def test_index_content(self):
        tester = self.WEB_APP.app.test_client()
        response = tester.get("/")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_form_in_index_source(self):
        tester = self.WEB_APP.app.test_client()
        response = tester.get("/")
        self.assertTrue(b"<form " in response.data)



if __name__ == "__main__":
    unittest.main()

