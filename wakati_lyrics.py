from constant import BOS, EOS, N_GRAM_NUMBER, TRACKS_FILE_NAME, UNK, WAKATI_FILE_NAME
from utils import phonetic2strvowels
from janome.tokenizer import Tokenizer
import pandas as pd
import csv

tokenizer = Tokenizer("user_dictionary.csv", udic_type="simpledic", udic_enc="utf8")

def wakati_lyrics(seq_lst):
  n_gram_lst = []
  for n in range(2, N_GRAM_NUMBER+1):
    for seq in seq_lst:
      token_lst = [token for token in tokenizer.tokenize(seq)]
      for i in range(len(token_lst)-n+1):
        surfaces = BOS + ' '
        vowels = BOS + ' '
        is_unk = False
        for token in token_lst[i:i+n]:
          surfaces += token.surface + ' '
          vowel = phonetic2strvowels(token.phonetic)
          if vowel == UNK:
            is_unk = True
            break
          vowels += vowel + ' '
        if is_unk:
          continue
        surfaces += EOS
        vowels += EOS
        n_gram_lst.append({
          'vowels': vowels,
          'lyrics': surfaces
        })
  return n_gram_lst

def store_wakati_file(filename, n_gram_lst):
  with open(filename, 'w') as f:
    writer = csv.DictWriter(f, ['vowels', 'lyrics'])
    writer.writeheader()
    for n_gram in n_gram_lst:
      writer.writerow(n_gram)

if __name__ == "__main__":
  df = pd.read_csv(TRACKS_FILE_NAME)
  df = df.dropna()
  lyrics_lst = list(df['lyrics'])
  n_gram_lst = wakati_lyrics(lyrics_lst)
  store_wakati_file(WAKATI_FILE_NAME, n_gram_lst)
