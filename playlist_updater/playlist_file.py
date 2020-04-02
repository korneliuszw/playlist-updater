import csv
import helpers
from copy import copy
import re
import os
csv_fields = ['title', 'upload_id', 'directory']
playlist_dir = helpers.get_playlist_directory()

def read_playlist_file(path):
    try:
        with open(path, 'r', newline='') as csvfile:
            data = csv.DictReader(csvfile, csv_fields)
            return list(data)[1:]
    except BaseException:
        return None



def get_playlist_file_name(playlist_name):
    return playlist_name.replace(' ', '_')


def remove_files(files_dic):
    for element in files_dic:
        try:
            path = element['directory']
            path = path.replace('"', '\'')
            os.remove(path + '.wav')
        except BaseException:
            pass


class SavedPlaylist:
    def __init__(self, playlist_name, mpd_playlist=None):
        self.fixed_name = get_playlist_file_name(playlist_name)
        self.path = helpers.path_to_file(playlist_dir, self.fixed_name)
        self.saved_playlist = read_playlist_file(self.path)
        self.mpd_playlist_dir = mpd_playlist
    def compare_playlists(self, second_playlist, output_path, keep):
        # Make copy of value in self for easier removing found elements
        saved_playlist = copy(self.saved_playlist)
        playlist_copy = copy(second_playlist)
        self.output_path = output_path
        if not saved_playlist:
            self.saved_playlist = second_playlist
            return (0, second_playlist)
        for element in second_playlist:
            previous_element = helpers.find_dict(
                saved_playlist, 'upload_id', element['upload_id'])
            if previous_element:
                saved_playlist.remove(previous_element)
                playlist_copy.remove(element)
        if not keep:
            self.saved_playlist = helpers.remove_elements(
                self.saved_playlist, saved_playlist)
            remove_files(saved_playlist)
        self.saved_playlist = self.saved_playlist + playlist_copy
        return (len(saved_playlist), playlist_copy)

    def remove_failed(self, failed):
        self.saved_playlist = helpers.remove_elements(self.saved_playlist, failed)

    def save_playlist_file(self):
        # List of paths that will be saving into mpd playlist, if user wants to
        with open(self.path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, csv_fields)
            writer.writeheader()
            for row in self.saved_playlist:
                upload_id = row.get('upload_id') or row['id']
                title = row['title']
                directory = row.get('directory')
                if not directory:
                    directory = re.sub(r'"', '\'', os.path.join(self.output_path, title))
                writer.writerow({
                    'directory': directory,
                    'upload_id': upload_id,
                    'title': title
                })
            if self.mpd_playlist_dir:
                self.save_to_mpd()
    def save_to_mpd(self):
        with open(os.path.join(self.mpd_playlist_dir, self.fixed_name + '.m3u'), 'w') as mpd_file:
            # Lines to list
            for item in self.saved_playlist:
                mpd_file.write(item['title'].replace('"', '\'')+ '.wav\n')

    def save(self):
        return self.save_playlist_file()
