import requests

URL = 'http://proxed.duc.tf:30019/'
HEADERS = {'X-Forwarded-For':'31.33.33.7'}
PARAMS = {}

r = requests.get(url = URL, params = PARAMS, headers = HEADERS)

text = r.text

print(text)