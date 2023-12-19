import requests
import regex
from bs4 import BeautifulSoup

class lastfm:
    def __init__(self, user: str):
        self.user = user
        self._url = "https://www.last.fm/"
        self._user_url = self._url + "user/"

    def check_user(self):
        req = requests.Session()
        rget = req.get(self._user_url + self.user, verify=True)
        bs = BeautifulSoup(rget.text, "html.parser")
        title = bs.find("span", {"class": "header-title-display-name"})
        # remove new line
        if title is not None:
            # don't ask me how it's works
            title = title.text.replace("\n", "").lstrip().replace("                   ", "")
        scrob =  bs.find("span", {"class": "header-scrobble-since"})
        if scrob is not None:
            scrob = scrob.text.replace("\n", "").replace("\n", "").replace("                    ", "")
        about = bs.find("div", {"class": "about-me-header"}).find_next("p")
        if about is not None:
            about = about.text
        scrobbler = bs.find('div', class_='header-metadata-display').find('p').find('a').text
        artist = bs.find_all('div', class_='header-metadata-display')[1].find('p').find('a').text
        loved_tracks = bs.find_all('div', class_='header-metadata-display')[2].find('p').find('a').text
        req.close()
        return f"{title}{scrob} - About Me {about}\nScrobbes: {scrobbler} - Artist {artist} - Loved Tracks {loved_tracks}"

    def top_track(self):
        req = requests.Session()
        rget = req.get(self._user_url + self.user, verify=True)
        bs = BeautifulSoup(rget.text, "html.parser")
        top_track = bs.find("h4", {"class": "featured-item-heading"})
        if top_track is not None:
            top_track = top_track.text.strip().lstrip().rstrip().replace("\n", "")
        title_song = bs.find("a", {"class": "featured-item-name"})
        if title_song is not None:
            title_song = title_song.text.strip().lstrip().rstrip()
        artist = bs.find("a", {"class", "featured-item-artist"})
        if artist is not None:
            artist = artist.text.strip().lstrip().rstrip()
        req.close()
        return f"{top_track} - {title_song} - {artist}".lstrip("\n")

d = lastfm("").top_track()
print(d)
#with open("a.txt", "w", encoding="utf-8") as f:
#    f.write(str(d))

