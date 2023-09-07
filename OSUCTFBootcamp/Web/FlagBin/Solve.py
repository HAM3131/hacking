import requests
from lxml import etree
from tqdm import tqdm

def get_sitemap_urls(url):
    try: 
        resp = requests.get(url)
        tree = etree.fromstring(resp.content)
        return [loc.text for loc in tree.findall('{*}url/{*}loc')]
    except requests.exceptions.RequestException:
        return []     

URL = ""
PARAMS = {}
HEADERS = {}
COOKIES = {}

hits = []

for URL in tqdm(get_sitemap_urls("https://flagbin-1.pwn.osucyber.club/sitemap.xml")):
    URL = "https://flagbin-1.pwn.osucyber.club/"+URL[len("http://pwn.osucyber.club:13399/"):]
    r = requests.get(url = URL, params = PARAMS, headers=HEADERS, cookies=COOKIES)
    text = r.text
    if (r.text.find("osuctf")!= -1):
        hits.append(URL)

print("Flag is at: ", hits)