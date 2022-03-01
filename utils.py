import pandas as pd
from constant import UNK
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

def phonetic2vowels(phonetic):
  if phonetic == '<bos>' or phonetic == '<eos>':
    return phonetic

  kana2vowel = {
    'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
    'カ': 'a', 'キ': 'i', 'ク': 'u', 'ケ': 'e', 'コ': 'o',
    'サ': 'a', 'シ': 'i', 'ス': 'u', 'セ': 'e', 'ソ': 'o',
    'タ': 'a', 'チ': 'i', 'ツ': 'u', 'テ': 'e', 'ト': 'o',
    'ナ': 'a', 'ニ': 'i', 'ヌ': 'u', 'ネ': 'e', 'ノ': 'o',
    'ハ': 'a', 'ヒ': 'i', 'フ': 'u', 'ヘ': 'e', 'ホ': 'o',
    'マ': 'a', 'ミ': 'i', 'ム': 'u', 'メ': 'e', 'モ': 'o',
    'ヤ': 'a', 'ユ': 'u', 'ヨ': 'o',
    'ラ': 'a', 'リ': 'i', 'ル': 'u', 'レ': 'e', 'ロ': 'o',
    'ワ': 'a', 'ヲ': 'o', 'ン': 'n', 'ヴ': 'u',
    'ガ': 'a', 'ギ': 'i', 'グ': 'u', 'ゲ': 'e', 'ゴ': 'o',
    'ザ': 'a', 'ジ': 'i', 'ズ': 'u', 'ゼ': 'e', 'ゾ': 'o',
    'ダ': 'a', 'ヂ': 'i', 'ヅ': 'u', 'デ': 'e', 'ド': 'o',
    'バ': 'a', 'ビ': 'i', 'ブ': 'u', 'ベ': 'e', 'ボ': 'o',
    'パ': 'a', 'ピ': 'i', 'プ': 'u', 'ペ': 'e', 'ポ': 'o',
    'ァ': 'a', 'ィ': 'i', 'ゥ': 'u', 'ェ': 'e', 'ォ': 'o',
    'ッ': 't', 'ャ': 'a', 'ュ': 'u', 'ョ': 'o',
  }

  lowchar = ['ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ャ', 'ュ', 'ョ']
  phonetic = phonetic.replace('ー', '')
  del_chars = [i for i, char in enumerate(phonetic[1:]) if char in lowchar]
  del_chars.reverse()
  for i in del_chars:
    phonetic = phonetic[:i] + phonetic[i+1:]
  vowels = [kana2vowel[char] if char in kana2vowel else UNK for char in phonetic]

  return vowels

def phonetic2strvowels(phonetic):
  return ''.join(phonetic2vowels(phonetic))

def load_dataset(filename):
  df = pd.read_csv(filename)
  df = df.dropna()
  vowels_lst = list(df['vowels'])
  lyrics_lst = list(df['lyrics'])
  return vowels_lst, lyrics_lst

def build_vocabulary(texts, num_words=None):
  tokenizer = tf.keras.preprocessing.text.Tokenizer(
    num_words=num_words, oov_token=UNK, filters=''
  )
  tokenizer.fit_on_texts(texts)
  return tokenizer

def create_dataset(vowels_texts, lyrics_texts, vowels_vocab, lyrics_vocab):
  vowels_seqs = vowels_vocab.texts_to_sequences(vowels_texts)
  lyrics_seqs = lyrics_vocab.texts_to_sequences(lyrics_texts)
  vowels_seqs = pad_sequences(vowels_seqs, padding='post')
  lyrics_seqs = pad_sequences(lyrics_seqs, padding='post')
  return [vowels_seqs, lyrics_seqs[:, :-1]], lyrics_seqs[:, 1:]
