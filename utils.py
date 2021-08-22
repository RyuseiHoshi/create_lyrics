def phonetic2vowels(word):
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

  word = word.replace('ン', '')
  word = word.replace('ッ', '')
  word = word.replace('ー', '')
  del_chars = [i for i, char in enumerate(word[1:]) if char in lowchar]
  del_chars.reverse()
  for i in del_chars:
    word = word[:i] + word[i+1:]
  vowels = [kana2vowel[char] for char in word if char in kana2vowel]

  return vowels
