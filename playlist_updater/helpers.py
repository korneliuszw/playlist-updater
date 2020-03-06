import os


def get_directory(path):
    os.listdir(path)


def get_playlist_directory():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    return file_dir.replace('/playlist_updater', '/.playlists')


def find_dict(dict_list, key, value):
    for element in dict_list:
        if element[key] == value:
            return element
    return None


def remove_elements(ar, elements):
    for element in elements:
        ar.remove(element)
    return ar


def path_to_file(directory, file_name):
    return "{}/{}".format(directory, file_name)


def create_directory():
    path = get_playlist_directory()
    print(path)
    if not os.path.isdir(path):
        print('no lol')
        os.mkdir(path)
    else:
        print('exists')

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    INFO = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
