import platform
import os
from helpers import colors


class Logger:
    notify = False

    def __init__(self, notify=False):
        if notify and platform.system() == "Linux":
            self.notify = True

    def send_notification(self, content):
        if self.notify:
            os.system('notify-send "Playlist updates" "{}"'.format(content))

    def error(self, message):
        self.send_notification("Failed to update playlist")
        print(f"{colors.FAIL}[ERROR] {message}{colors.ENDC}")

    def info(self, message):
        print(f"{colors.INFO}[INFO] {message} {colors.ENDC}")

    def finish(self, message):
        self.send_notification(message)
        print(f"{colors.OKGREEN}[SUCCESS] {message} {colors.ENDC}")
