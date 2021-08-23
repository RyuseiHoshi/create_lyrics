from constant import TRACKS_FILE_NAME, WAKATI_FILE_NAME
from utils import phonetic2strvowels
from janome.tokenizer import Tokenizer
import pandas as pd
import csv

tokenizer = Tokenizer()

def wakati_lyrics(seq_lst):
  morphemes = []
  for seq in seq_lst:
    surfaces = '<BOS> '
    vowels = '<BOS> '
    for token in tokenizer.tokenize(seq):
      surfaces += token.surface + ' '
      vowels += phonetic2strvowels(token.phonetic) + ' '
    surfaces += '<EOS>'
    vowels += '<EOS>'
    morphemes.append({
      'surface': surfaces,
      'vowels': vowels
    })
  return morphemes
  
def store_wakati_file(filename, morphemes):
  with open(filename, 'w') as f:
    writer = csv.DictWriter(f, ['vowels', 'surface'])
    writer.writeheader()
    for morpheme in morphemes:
      writer.writerow(morpheme)

if __name__ == "__main__":
  df = pd.read_csv(TRACKS_FILE_NAME)
  df = df.dropna()
  lyrics_lst = list(df['lyrics'])
  morphemes = wakati_lyrics(lyrics_lst)
  store_wakati_file(WAKATI_FILE_NAME, morphemes)
