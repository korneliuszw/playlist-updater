#!/usr/bin/python
from youtube_dl import YoutubeDL
import argparse
import os
from playlist_file import SavedPlaylist
from logger import Logger
from helpers import create_directory
import scrapper;

parser = argparse.ArgumentParser(
    description='Download from youtube playlist that are not present in output folder')
parser.add_argument(
    'output_dir',
    type=str,
    help="Directory to which content of playlist would be saved.")
parser.add_argument('playlist_url', type=str, help="Link to the playlist")
parser.add_argument(
    '-k',
    '--keep-removed',
    action='store_true',
    default=False,
    help="Keep removed playlist elements")
parser.add_argument(
    '-n',
    '--notify',
    action='store_true',
    default=False,
    help="Send notification (by notify-send) about playlist updates.")
parser.add_argument(
    '-p',
    '--mpd-playlist-dir',
    type=str,
    help="Path to mpd playlist directory. Optional")
def main(args, logger):
    create_directory()
    ytdl = YoutubeDL({
        'quiet': True,
        'prefer_insecure': True,
        'outtmpl': os.path.join(args.output_dir, '%(title)s.wav'),
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav'
        }],
        'keepvideo': False
    })
    logger.info("Fetching playlist (this can take a while)")
    playlist_name, playlist = scrapper.get_playlist_details(args.playlist_url)
    saved_playlist = SavedPlaylist(playlist_name.lstrip().rstrip(), args.mpd_playlist_dir)
    removed_elements, remaining_elements = saved_playlist.compare_playlists(
        playlist, args.output_dir, args.keep_removed)
    if (removed_elements > 0):
        logger.info('{} elements were removed from playlist'.format(removed_elements))
    new_elements = len(remaining_elements)
    logger.info("Found {} new elements, downloading...".format(new_elements))
    for i in range(0, new_elements):
        try:
            ytdl.download(
                ['https://youtube.com/watch?v={}'.format(remaining_elements[i]['upload_id'])])
        except Exception as e:
            logger.error(e)
            saved_playlist.remove_failed(remaining_elements[i:])
            saved_playlist.save()
    saved_playlist.save()
    if new_elements > 0:
        logger.finish("{} new elements added".format(new_elements))

args = parser.parse_args()
logger = Logger(args.notify)
try:
    main(args, logger)
except Exception as e:
    logger.error(e)

