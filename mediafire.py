import requests
from bs4 import BeautifulSoup

def get_media_fire(url: str):
    r = requests.get(url)
    re_re = BeautifulSoup(r.text, "html.parser")
    anchor_tag = re_re.find('a', class_='input popsok')
    return anchor_tag["href"]

d = get_media_fire()
print(d)
