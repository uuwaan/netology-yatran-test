import os
import unittest

import requests

_API_URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"

_HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(_HERE, "yatran_key.txt"), "r") as api_file:
    _YATRAN_KEY = api_file.readline().strip()


class TestYaTranResults(unittest.TestCase):
    def test_without_api_key(self):
        req_params = {"text": "Test", "lang": "en-ru"}
        resp = requests.get(_API_URL, params=req_params)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {
            "code": 502,
            "message": "Invalid parameter: key",
        })

    def test_with_empty_api_key(self):
        req_params = {"key": "", "text": "Test", "lang": "en-ru"}
        resp = requests.get(_API_URL, params=req_params)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json(), {
            "code": 401,
            "message": "API key is invalid",
        })

    def test_with_proper_trdir(self):
        req_params = {"key": _YATRAN_KEY, "text": "Hello", "lang": "en-ru"}
        resp = requests.get(_API_URL, params=req_params)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            "code": 200,
            "lang": "en-ru",
            "text": ["Привет"],
        })

    def test_with_wrong_trdir(self):
        req_params = {"key": _YATRAN_KEY, "text": "Hello", "lang": "en-zz"}
        resp = requests.get(_API_URL, params=req_params)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {
            "code": 501,
            "message": "The specified translation direction is not supported",
        })

    def test_with_auto_lang(self):
        req_params = {"key": _YATRAN_KEY, "text": "Hallo", "lang": "ru"}
        resp = requests.get(_API_URL, params=req_params)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            "code": 200,
            "lang": "de-ru",
            "text": ["Привет"],
        })

    def test_with_fake_notranslit_lang(self):
        req_params = {"key": _YATRAN_KEY, "text": "Hola", "lang": "it-ru"}
        resp = requests.get(_API_URL, params=req_params)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            "code": 200,
            "lang": "it-ru",
            "text": ["Hola"],
        })

    def test_with_fake_translit_lang(self):
        req_params = {"key": _YATRAN_KEY, "text": "Hola", "lang": "en-ru"}
        resp = requests.get(_API_URL, params=req_params)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {
            "code": 200,
            "lang": "en-ru",
            "text": ["Хола"],
        })
