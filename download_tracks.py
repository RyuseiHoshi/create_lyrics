from constant import ARTIST_NAME, TRACKS_FILE_NAME
from musixmatch import Musixmatch
import re
import json
import csv

with open('secret.json') as f:
  secret = json.load(f)

musixmatch = Musixmatch(secret['MUSIXMATCH_API_KEY'])

def get_lyrics(track_id):
  res = musixmatch.track_lyrics_get(track_id)
  lyrics = res['message']['body']['lyrics']['lyrics_body']
  lyrics = re.sub(r'（.*?）', ' ', lyrics)
  lyrics = re.sub(r'\(\d+\)', ' ', lyrics)
  lyrics = re.sub(r'\\n', ' ', lyrics)
  lyrics = re.sub(r'\s', '', lyrics)
  lyrics = lyrics.replace('...*******ThisLyricsisNOTforCommercialuse*******', '')
  return lyrics

def get_tracks_from_artist(artistname):
  res = musixmatch.track_search(q_artist=artistname, page_size=1000, page=1, s_track_rating='desc', q_track='')
  track_list = res['message']['body']['track_list']
  tracks = [{
    'track_id': track['track']['track_id'],
    'track_name': track['track']['track_name'],
    'artist_name': track['track']['artist_name'],
    'lyrics': get_lyrics(track['track']['track_id'])
    } for track in track_list]
  return tracks

def store_tracks_file(filename, tracks):
  with open(filename, 'w') as f:
    writer = csv.DictWriter(f, ['track_id', 'track_name', 'artist_name', 'lyrics'])
    writer.writeheader()
    for track in tracks:
      writer.writerow(track)

if __name__ == "__main__":
  tracks = get_tracks_from_artist(ARTIST_NAME)
  store_tracks_file(TRACKS_FILE_NAME, tracks)
