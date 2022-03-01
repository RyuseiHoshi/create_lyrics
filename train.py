from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np
from inference import InferenceAPI, InferenceAPIforAttention
from models import Seq2seq, Encoder, Decoder, AttentionDecoder
from utils import load_dataset, build_vocabulary, create_dataset
from constant import WAKATI_FILE_NAME

def main():
  batch_size = 32
  epochs = 100
  model_path = 'models/model.h5'
  enc_arch = 'models/encoder.json'
  dec_arch = 'models/decoder.json'
  num_words = 10000
  num_data = 20000

  vowels_lst, lyrics_lst = load_dataset(WAKATI_FILE_NAME)
  vowels_lst, lyrics_lst = vowels_lst[:num_data], lyrics_lst[:num_data]

  x_train, y_train = np.array(lyrics_lst), np.array(lyrics_lst)
  vowels_vocab = build_vocabulary(x_train, num_words)
  lyrics_vocab = build_vocabulary(y_train, num_words)
  x_train, y_train = create_dataset(x_train, y_train, vowels_vocab, lyrics_vocab)

  encoder = Encoder(num_words, return_sequences=True)
  decoder = AttentionDecoder(num_words)
  seq2seq = Seq2seq(encoder, decoder)
  model = seq2seq.build()
  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

  callbacks = [
    EarlyStopping(patience=3),
    ModelCheckpoint(model_path, save_best_only=True, save_weights_only=True)
  ]
  model.fit(x=x_train,
        y=y_train,
        batch_size=batch_size,
        epochs=epochs,
        callbacks=callbacks,
        validation_split=0.1)
  encoder.save_as_json(enc_arch)
  decoder.save_as_json(dec_arch)

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
