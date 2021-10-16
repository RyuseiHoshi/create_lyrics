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
    output, state = self.decoder_model.predict([target_seq, state])
    return output, state

  def _generate_sequence(self, enc_output, state, max_seq_len=50):
    """Generate a sequence.

    Args:
      states: initial states of the decoder.

    Returns:
      sampled: a generated sequence.
    """
    target_seq = np.array([self.lyrics_vocab.word_index['<bos>']])
    sequence = []
    for i in range(max_seq_len):
      output, state = self._compute_decoder_output(target_seq, state, enc_output)
      sampled_tokvowels_index = np.argmax(output[0, 0])
      if sampled_tokvowels_index == self.lyrics_vocab.word_index['<eos>']:
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
    output, state = self.decoder_model.predict([target_seq, enc_output, state])
    return output, state
