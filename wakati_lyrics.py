from constant import FILE_NAME, WAKATI_FILE_NAME
from utils import load_dataset, phonetic2vowels
from janome.tokenizer import Tokenizer
import pandas as pd
import csv

tokenizer = Tokenizer()

def wakati_lyrics(filename, seq_lst):
  morphemes = []
  for seq in seq_lst:
    morphemes += [{'surface': '<BOS>', 'vowels': '<BOS>'}]
    morphemes += [{
      'surface': token.surface,
      'vowels': ''.join(phonetic2vowels(token.phonetic))
    } for token in tokenizer.tokenize(seq)]
    morphemes += [{'surface': '<EOS>', 'vowels': '<EOS>'}]
  
  with open(filename, 'w') as f:
    writer = csv.DictWriter(f, ['surface', 'vowels'])
    writer.writeheader()
    for morpheme in morphemes:
      writer.writerow(morpheme)

if __name__ == "__main__":
  df = pd.read_csv(FILE_NAME)
  df = df.dropna()
  lyrics_lst = list(df['lyrics'])
  wakati_lyrics(WAKATI_FILE_NAME, lyrics_lst)
