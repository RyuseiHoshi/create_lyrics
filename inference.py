"""
Inference API.
"""
import numpy as np

class InferenceAPI:
  """A model API that generates output sequence.

  Attributes:
    encoder_model: Model.
    decoder_model: Model.
    vowels_vocab: source vowels's vocabulary.
    lyrics_vocab: target lyrics's vocabulary.
  """

  def __init__(self, encoder_model, decoder_model, vowels_vocab, lyrics_vocab):
    self.encoder_model = encoder_model
    self.decoder_model = decoder_model
    self.vowels_vocab = vowels_vocab
    self.lyrics_vocab = lyrics_vocab

  def predict(self, text):
    output, state = self._compute_encoder_output(text)
    sequence = self._generate_sequence(output, state)
    decoded = self._decode(sequence)
    return decoded

  def _compute_encoder_output(self, text):
    """Compute encoder output.

    Args:
      text : string, the input text.

    Returns:
      output: encoder's output.
      state : encoder's final state.
    """
    assert isinstance(text, str)
    x = self.vowels_vocab.texts_to_sequences([text])
    output, state = self.encoder_model.predict(x)
    return output, state

  def _compute_decoder_output(self, target_seq, state, enc_output=None):
    """Compute decoder output.

    Args:
      target_seq: target sequence.
      state: hidden state.
      output: encoder's output.

    Returns:
      output: decoder's output.
      state: decoder's state.
    """
    output, state = self.decoder_model.predict([Reshape((len(target_seq), 1))(target_seq), state])
    return output, state

  def _generate_sequence(self, enc_output, state, max_seq_len=50):
    """Generate a sequence.

    Args:
      states: initial states of the decoder.

    Returns:
      sampled: a generated sequence.
    """
    target_seq = np.array([self.lyrics_vocab.word_index[BOS]])
    sequence = []
    for i in range(max_seq_len):
      output, state = self._compute_decoder_output(target_seq, state, enc_output)
      sampled_tokvowels_index = np.argmax(output[0, 0])
      if sampled_tokvowels_index == self.lyrics_vocab.word_index[EOS]:
        break
      sequence.append(sampled_tokvowels_index)
      target_seq = np.array([sampled_tokvowels_index])
    return sequence

  def _decode(self, sequence):
    """Decode a sequence.

    Args:
      sequence: a generated sequence.

    Returns:
      decoded: a decoded sequence.
    """
    decoded = self.lyrics_vocab.sequences_to_texts([sequence])
    decoded = decoded[0].split(' ')
    return decoded

class InferenceAPIforAttention(InferenceAPI):
  def _compute_decoder_output(self, target_seq, state, enc_output=None):
    output, state = self.decoder_model.predict([Reshape((len(target_seq), 1))(target_seq), enc_output, state])
    return output, state


from tensorflow.keras.layers import Reshape
from models import Seq2seq, Encoder, Decoder, AttentionDecoder
from utils import load_dataset, build_vocabulary, create_dataset
from constant import BOS, EOS, WAKATI_FILE_NAME

def main():
  model_path = 'models/model.h5'
  enc_arch = 'models/encoder.json'
  dec_arch = 'models/decoder.json'
  num_words = 10000
  num_data = 20000

  vowels_lst, lyrics_lst = load_dataset(WAKATI_FILE_NAME)
  vowels_lst, lyrics_lst = vowels_lst[:num_data], lyrics_lst[:num_data]

  vowels_vocab = build_vocabulary(np.array(lyrics_lst), num_words)
  lyrics_vocab = build_vocabulary(np.array(lyrics_lst), num_words)

  encoder = Encoder.load(enc_arch, model_path)
  decoder = Decoder.load(dec_arch, model_path)
  api = InferenceAPIforAttention(encoder, decoder, vowels_vocab, lyrics_vocab)

  texts = sorted(set(vowels_lst[:50]), key=len)
  for text in texts:
    decoded = api.predict(text=text)
    print('Vowels : {}'.format(text))
    print('Lyrics: {}'.format(decoded))

if __name__ == '__main__':
  main()
