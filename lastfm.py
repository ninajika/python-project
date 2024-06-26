import requests
import regex
import json
from bs4 import BeautifulSoup

class lastfmProfile:
    def __init__(self, user: str):
        self.user = user
        self._url = "https://www.last.fm/"
        self._user_url = f"{self._url}user/"
        self._headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 14469.59.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
        }

    # removed after finish
    def base_for_research(self):
        req = requests.Session()
        rget = req.get(self._user_url + self.user, headers=self._headers, verify=True)
        bs = BeautifulSoup(rget.text, "html.parser")
        req.close()
        return bs

    def check_user(self):
        req = requests.Session()
        rget = req.get(self._user_url + self.user, headers=self._headers, verify=True)
        bs = BeautifulSoup(rget.text, "html.parser")
        title = bs.find("span", {"class": "header-title-display-name"})
        # remove new line
        if title is not None:
            # don't ask me how it's works
            title = title.text.replace("\n", "").lstrip().replace("                   ", "")
        else:
            title = None
        scrob =  bs.find("span", {"class": "header-scrobble-since"})
        if scrob is not None:
            scrob = scrob.text.replace("\n", "").replace("\n", "").replace("                    ", "")
        else:
            scrob = None
        about = bs.find("div", {"class": "about-me-header"})
        if about is not None:
            about = about.find_next("p").text.replace("read more", "").strip().lstrip().rstrip()
        else:
            about = None
        profile_picture = bs.find("div", {"class": "expand-image-show-on-focus header-avatar-inner-wrap"})
        if profile_picture is not None:
            profile_picture = profile_picture.find("img").get("src")
        else:
            profile_picture = None
        scrobbler = bs.find('div', class_='header-metadata-display').find('p').find('a').text
        artist = bs.find_all('div', class_='header-metadata-display')[1].find('p').find('a').text
        try:
            loved_tracks = bs.find_all('div', class_='header-metadata-display')[2]
            loved_tracks = loved_tracks.find('p').find('a').text
        except IndexError:
            loved_tracks = None
        req.close()
        return f"{title}{scrob} - About Me {about}\n\nScrobbes: {scrobbler} - Artist {artist} - Loved Tracks {loved_tracks}\nLink Profile - {self._url}user/{self.user}\nPhoto Profile - {profile_picture}"

    def top_track(self):
        req = requests.Session()
        rget = req.get(self._user_url + self.user, headers=self._headers, verify=True)
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
        scrobble = bs.find("span", {"class": "chartlist-count-bar-value"})
        if scrobble is not None:
            scrobble = scrobble.text.strip().lstrip().rstrip().replace("scrobbles", "")
        req.close()
        # return scrobble
        return f"{top_track}\nResult {title_song} - {artist} | {scrobble}scrobbles".lstrip("\n")


    def get_artist_and_plays(self):
        req = requests.Session()
        rget = req.get(self._user_url + self.user, headers=self._headers, verify=True)
        bs = BeautifulSoup(rget.text, "html.parser")
        artists = [lastfmutils.clean_result(art.text) for art in bs.find_all('p', class_='grid-items-item-main-text')]
        plays = [lastfmutils.clean_result(play.text) for play in bs.find_all('p', class_='grid-items-item-aux-text')]
        req.close()

        return artists, plays

    def top_artists(self):
        artists, plays = self.get_artist_and_plays()
        result = []
        min_length = min(len(artists), len(plays))

        for i in range(min_length):
            if "plays" in plays[i]:
                results = {
                    "artist": artists[i],
                    "many_played": plays[i]
                }
                result.append(results)

        return json.dumps(result[:int(min_length/2)])

    def top_albums(self):
        artists, plays = self.get_artist_and_plays()
        result = []
        min_length = min(len(artists), len(plays))

        for i in range(min_length):
            if "plays" in plays[i] and not plays[i].startswith(artists[i]):
                play_split = plays[i].split(' ')
                album_play_count = play_split[-2] + ' ' + play_split[-1]  # E.g., "4 plays"
                album_artist = ' '.join(play_split[:-2])  # The rest is the artist's name

                results = {
                    "title": artists[i],
                    "artist": album_artist,
                    "many_plays": album_play_count
                }
                result.append(results)

        return json.dumps(result[int(min_length/2):int(min_length)])

    def recent_track(self):
        req = requests.Session()
        rget = req.get(self._user_url + self.user, headers=self._headers, verify=True)
        bs = BeautifulSoup(rget.text, "html.parser")

        title_songs = [td.a['title'] for td in bs.find_all('td', class_='chartlist-name')]
        artist_songs = [td.a.text for td in bs.find_all('td', class_='chartlist-artist')]
        album_arts = [td.img['src'] for td in bs.find_all('td', class_='chartlist-image')]
        when_i_listen = [lastfmutils.clean_result(td.span.text) for td in bs.find_all('td', class_='chartlist-timestamp')]

        results = []
        seen_tracks = set() # make less duplicated data
        min_length = min(len(title_songs), len(artist_songs), len(album_arts), len(when_i_listen))

        for i in range(min_length):
            track_id = (title_songs[i], artist_songs[i])
            if track_id not in seen_tracks:
                seen_tracks.add(track_id)
                result = {
                    "Title": title_songs[i],
                    "Artist": artist_songs[i],
                    "Album Art": album_arts[i],
                    "When i listen": when_i_listen[i]
                }
                results.append(result)

        req.close()
        return json.loads(json.dumps(results))

class lastfmutils:
    def __init__(self) -> None:
        pass

    # @staticmethod
    # def spacer(str):
    #
    #     sentence = []                 # create empty list
    #
    #     sentence.append(str[0])       # put first letter in list. First letter doesn't need a space.
    #     for char in str[1::]:         # begin iteration after first letter
    #         if char.islower():
    #             sentence.append(char) # if character is lower add to list
    #         elif char.isupper():
    #             sentence.append( " ") # if character is upper add a space to list
    #             sentence.append(char) # then add the upper case character to list
    #     result = ''.join(sentence)    # use () join to convert the list to a string
    #     return result                 # return end result
    #


    @staticmethod
    def clean_result(result: str) -> str:
        """
        Cleans the given result by removing newline characters, multiple consecutive spaces, and leading/trailing spaces.

        Parameters:
            result (str): The result string to be cleaned.

        Returns:
            str: The cleaned result string.
        """
        result = result.replace("\n", "")
        result = regex.sub(r"\n+", " ", result)
        result = regex.sub(r"\s+", " ", result)
        result = result.lstrip().rstrip()
        return result

d = lastfmProfile("lasapeur").top_artists()
print(d)
# print(d)
# with open("a.txt", "w", encoding="utf-8") as f:
#     f.write(str(d))

