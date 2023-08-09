"""
特定のアーティストの楽曲情報と歌詞を取得し、CSVファイルに保存する役割を持っている
"""

from constant import ARTIST_NAME, TRACKS_FILE_NAME # 'constant.py'ファイルから'ARTIST_NAME'と'TRACKS_FILE_NAME'の定数をインポート
                                                   # これらの定数はアーティストの名前と楽曲情報を保存するためのcsvファイル名を示している
from musixmatch import Musixmatch # 'musixmatch'ライブラリから'Musixmatch'クラスwおインポートしている。
                                  # これはMusixmatch APIとの連携を可能にする
import re
import json
import csv

with open('secret.json') as f: # 'secret.json'ファイルを読み込んでAPIキーを取得する。このファイルには、Musixmatch APIのアクセスに必要な情報が含まれている。
  secret = json.load(f)

musixmatch = Musixmatch(secret['MUSIXMATCH_API_KEY']) # 取得したAPIキーを使用してMusixmatchクラスのインスタンスを作成

def get_lyrics(track_id): # 与えられたトラックIDに対応する歌詞を取得する関数。取得した歌詞はいくつかの正規表現と文字列操作によって整形される
  res = musixmatch.track_lyrics_get(track_id)
  lyrics = res['message']['body']['lyrics']['lyrics_body']
  lyrics = re.sub(r'（.*?）', ' ', lyrics)
  lyrics = re.sub(r'\(\d+\)', ' ', lyrics)
  lyrics = re.sub(r'\\n', ' ', lyrics)
  lyrics = re.sub(r'\s', '', lyrics)
  lyrics = lyrics.replace('...*******ThisLyricsisNOTforCommercialuse*******', '')
  return lyrics

def get_tracks_from_artist(artistname): # 特定のアーティストの楽曲情報を取得する関数。'musixmatch.track_search'を使用してアーティストに関連する楽曲情報を取得し、歌詞も含めて辞書形式で整理
  res = musixmatch.track_search(q_artist=artistname, page_size=1000, page=1, s_track_rating='desc', q_track='')
  track_list = res['message']['body']['track_list']
  tracks = [{
    'track_id': track['track']['track_id'],
    'track_name': track['track']['track_name'],
    'artist_name': track['track']['artist_name'],
    'lyrics': get_lyrics(track['track']['track_id'])
    } for track in track_list]
  return tracks

def store_tracks_file(filename, tracks): # 楽曲譲歩をCSVファイルに保存する関数。指定されたファイル名でCSVファイルを作成し、'csv.DictWriter'を使用して辞書のリストをCSVファイルに書き込む
  with open(filename, 'w') as f:
    writer = csv.DictWriter(f, ['track_id', 'track_name', 'artist_name', 'lyrics'])
    writer.writeheader()
    for track in tracks:
      writer.writerow(track)

if __name__ == "__main__": # スクリプトが直接実行された場合のみ以下のコードが実行されるようにする
  tracks = get_tracks_from_artist(ARTIST_NAME) # 'ARTIST_NAME'で指定されたアーティストの楽曲情報を取得
  store_tracks_file(TRACKS_FILE_NAME, tracks) # 取得した楽曲情報を指定されたファイル名でCSVファイルに保存


"""
Musixmatch APIを使用してアーティストの楽曲情報と歌詞を取得し、指定されたCSVファイルに保存する役割を果たす。
ただし、正常に動作されるためには'secret.json'ファイルが存在し、APIキーが正しく設定される必要がある。
"""
