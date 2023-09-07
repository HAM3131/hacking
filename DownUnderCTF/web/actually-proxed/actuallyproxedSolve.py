# This is an incomplete solution -- (it doesn't work and is entirely based on the `proxed` challenge)

import requests

URL = 'http://actually.proxed.duc.tf:30009/'
HEADERS = {'x-forwarded-for':'31.33.33.7'}
PARAMS = {}

r = requests.get(url = URL, params = PARAMS, headers = HEADERS)

text = r.text

print(text)