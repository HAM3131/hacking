import requests
from lxml import etree

def get_sitemap_urls(url):
    try: 
        resp = requests.get(url)
        tree = etree.fromstring(resp.content)
        return [loc.text for loc in tree.findall('{*}url/{*}loc')]
    except requests.exceptions.RequestException:
        return []
    
