# Save and update your youtube playlists automatically
Use this script to get the latest changes for your youtube playlist.
You can schedule running this script on reboot // TODO: Make a tutorial

## Requirements
   - Python 3
   - [Youtube-DL](https://ytdl-org.github.io/youtube-dl/download.html) module

## Main Features
   - Download new elements that have been added to your playlist
   - Remove elements that are no longer in the playlist
   - Save playlist information as MPD playlist (optional)
   - Send notifications via notify-send about succesfull or not updates
## Running

```bash
python playlist_updater/playlist_updater.py <PATH_TO_DESTINATION_FOLDER> '<LINK TO YOUTUBE PLAYLIST>'
```

## Command line arguments:
   | Argument              | Description                                                        | Expected Value |
   | ---                   | ---                                                                | ---            |
   | output_dir            | Directory to which everything will be saved                        | string         |
   | playlist_url          | Link to your playlist                                              | string         |
   | -k --keep-removed     | Keep removed elements on disk. Optional                            | none           |
   | -n --notify           | Send notifications via notify-send. Optional;                      | none           |
   | -p --mpd-playlist-dir | Mpd playlist directory (e.g $HOME/.config/mpd/playlists). Optional | string         |

## TODO
   - Save logs to file
   - Scheduling updates
   - Better optimization
   - Better documentation
