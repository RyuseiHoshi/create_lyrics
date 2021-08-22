from musixmatch import Musixmatch
from pprint import pprint
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

def get_tracks_from_artist(artist_name):
  res = musixmatch.track_search(q_artist=artist_name, page_size=1000, page=1, s_track_rating='desc', q_track='')
  track_list = res['message']['body']['track_list']
  tracks = [{
    'track_id': track['track']['track_id'],
    'track_name': track['track']['track_name'],
    'lyrics': get_lyrics(track['track']['track_id'])
    } for track in track_list]
  return tracks

def download_lyrics_from_artist(artist_name, file_name):
  tracks = get_tracks_from_artist(artist_name)
  with open(file_name, 'w') as f:
    writer = csv.DictWriter(f, ['track_id', 'track_name', 'lyrics'])
    writer.writeheader()
    for track in tracks:
      writer.writerow(track)

# print('artist name: ', end='')
# artist_name = input()
# print('file name: ', end='')
# file_name = input()
artist_name = 'Kenshi Yonezu'
file_name = 'Kenshi-Yonezu-tracks.csv'
download_lyrics_from_artist(artist_name, file_name)
