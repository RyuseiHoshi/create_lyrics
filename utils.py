def phonetic2vowels(phonetic):
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
    'ワ': 'a', 'ヲ': 'o', 'ヴ': 'u',
    'ガ': 'a', 'ギ': 'i', 'グ': 'u', 'ゲ': 'e', 'ゴ': 'o',
    'ザ': 'a', 'ジ': 'i', 'ズ': 'u', 'ゼ': 'e', 'ゾ': 'o',
    'ダ': 'a', 'ヂ': 'i', 'ヅ': 'u', 'デ': 'e', 'ド': 'o',
    'バ': 'a', 'ビ': 'i', 'ブ': 'u', 'ベ': 'e', 'ボ': 'o',
    'パ': 'a', 'ピ': 'i', 'プ': 'u', 'ペ': 'e', 'ポ': 'o',
    'ァ': 'a', 'ィ': 'i', 'ゥ': 'u', 'ェ': 'e', 'ォ': 'o', 'ャ': 'a', 'ュ': 'u', 'ョ': 'o',
  }

  lowchar = ['ァ', 'ィ', 'ゥ', 'ェ', 'ォ', 'ャ', 'ュ', 'ョ']

  phonetic = phonetic.replace('ン', '')
  phonetic = phonetic.replace('ッ', '')
  phonetic = phonetic.replace('ー', '')
  del_chars = [i for i, char in enumerate(phonetic[1:]) if char in lowchar]
  del_chars.reverse()
  for i in del_chars:
    phonetic = phonetic[:i] + phonetic[i+1:]
  vowels = [kana2vowel[char] if char in kana2vowel else '<NAN>' for char in phonetic]

  return vowels

def phonetic2strvowels(phonetic):
  return ''.join(phonetic2vowels(phonetic))
