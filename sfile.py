import requests
import re
from bs4 import BeautifulSoup

def sfile(url: str) -> str:
    sesi = requests.session()
    rek = sesi.get(url).text
    bs = BeautifulSoup(rek, "html.parser")
    dl_link = bs.find("a", class_= "w3-button w3-blue w3-round").get("href")
    rek = sesi.get(dl_link, headers={"referer": url, 'cache-control': 'max-age=0', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'})
    bs_1 = BeautifulSoup(rek.text, "html.parser")
    final_url = bs_1.find("a", {"id": "download"}).get("href")
    pattern = re.compile(r"location\.href=this\.href\+\'&k=\'\+\'([a-f0-9]{1,32})\'(?:;return\sfalse;)?")
    match = pattern.search(rek.text)
    if match:
        k_value = match.group(1)
    else:
        k_value = None
    return dl_link, f'{final_url}&k={k_value}'

print(sfile("https://sfile.mobi/AIsNZrb3vU7"))
