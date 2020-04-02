import requests
from bs4 import BeautifulSoup as SoupFactory
import threading
import helpers

def get_playlist_details(playlist_url):
    if (not helpers.is_youtube_playlist(playlist_url)):
        raise PlaylistWrongURLError(playlist_url, "Provided playlist url does not look like yt playlist")
    req = requests.get(playlist_url)
    if req.status_code != 200:
        req.raise_for_status()
    soup = SoupFactory(req.content, 'html.parser')
    playlist_name_element = soup.select('.pl-header-title')
    video_list = []
    for element_index in range(0, len(soup.select('tr.pl-video'))):
        element = soup.select(current_element_selector(element_index))
        video_id = element[0].get('data-video-id')
        title = element[0].get('data-title')
        video_list.append({
            'upload_id': video_id,
            'title': title})
    if (len(video_list) == 0):
        raise PlaylistEmptyError(playlist_url, "It seems like this playlist is empty.")
    return (playlist_name_element[0].get_text(), video_list)

def current_element_selector(index):
    return 'tr.pl-video:nth-child({})'.format(index + 1)

class PlaylistEmptyError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class PlaylistWrongURLError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

