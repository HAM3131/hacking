import requests

URL = ""
PARAMS = {}
HEADERS = {}
COOKIES = {}

r = requests.get(url = URL, params = PARAMS, headers=HEADERS, cookies=COOKIES)

text = r.text