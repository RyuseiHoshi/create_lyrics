from sklearn.model_selection import train_test_split # データセットをトレーニングデータとテストデータに分割する関数
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint # EarlyStopping:モデルの性能が改善しなくなった場合にトレーニングを停止する。ModelCheckpoint:モデルの重みを保存する。
from tensorflow.keras.utils import plot_model # この関数は、モデルの構造を可視化する
import numpy as np
import matplotlib.pyplot as plt
from inference import InferenceAPI, InferenceAPIforAttention
from models import Seq2seq, Encoder, Decoder, AttentionDecoder
from utils import load_dataset, build_vocabulary, create_dataset
from constant import ACC_HISTORY_FILE_NAME, LOSS_HISTORY_FILE_NAME, MODEL_IMAGE_FILE_NAME, WAKATI_FILE_NAME

def main():
  batch_size = 32 # 1回のバッチ処理で使用するデータの数
  epochs = 100 # トレーニングエポックの数
  model_path = 'models/model.h5' # モデルの重みを保存するファイルのパス
  enc_arch = 'models/encoder.json' # エンコーダモデルのアーキテクチャを保存するJSONファイルのパス
  dec_arch = 'models/decoder.json' # デコーダモデルのアーキテクチャを保存するJSONファイルのパス
  num_words = 10000 # 使用する語彙の数
  num_data = 20000 # 使用するデータの数

  vowels_lst, lyrics_lst = load_dataset(WAKATI_FILE_NAME) # 前処理済みのデータを読み込む。
  vowels_lst, lyrics_lst = vowels_lst[:num_data], lyrics_lst[:num_data] # データセットのサイズを'num_data'で制限し、必要なデータの数だけを残す

  x_train, y_train = np.array(lyrics_lst), np.array(lyrics_lst) # 'lyrics_lst'をNumPyの配列に変換し、'x_train'と'y_train'にそれぞれ格納する。
  vowels_vocab = build_vocabulary(x_train, num_words) # 'build_vocabulary'関数を使って、'x_train'の語彙を構築し、'vowels_vocab'に格納
  lyrics_vocab = build_vocabulary(y_train, num_words) # 'build_vocabulary'関数を使って、'y_train'の語彙を構築し、'lyrics_vocab'に格納
  x_train, y_train = create_dataset(x_train, y_train, vowels_vocab, lyrics_vocab) # 'create_dataset'関数を呼び出し、'x_train'と'y_train'をエンコードし、データセットを準備

  encoder = Encoder(num_words, return_sequences=True) # 'Encoder'クラスを呼び出し、'num_words'の語彙数を持つエンコーダを作成
  decoder = AttentionDecoder(num_words) # 'AttentionDecoder'クラスを呼び出し、'num_words'の語彙数を持つデコーダを作成
  seq2seq = Seq2seq(encoder, decoder) # 'Encoder'と'Decoder'を使用して'Seq2Seq'モデルを作成
  model = seq2seq.build() # 'Seq2Seq'モデルをビルド
  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy') # モデルをコンパイル。OptimizerはAdamを使用、損失関数として'sparse_categorical_crossentropy'を使用

  callbacks = [ # コールバックを定義
    EarlyStopping(patience=3), # 
    ModelCheckpoint(model_path, save_best_only=True, save_weights_only=True)
  ]
  history = model.fit(x=x_train, # モデルを訓練する。'x_train'および'y_train'を使用し、設定された'batch_size'および'epochs'でトレーニングを行う。また、前述のコールバックやバリエーションの割合なども指定。'fit'メソッドの戻り値として訓練の履歴が返される。
                  y=y_train,
                  batch_size=batch_size,
                  epochs=epochs,
                  callbacks=callbacks,
                  validation_split=0.1)
  encoder.save_as_json(enc_arch) # エンコーダモデルのアーキテクチャをJSONファイルに保存
  decoder.save_as_json(dec_arch) # デコーダモデルのアーキテクチャをJSONファイルに保存

  fig = plt.figure() # 新しい図を作成
  print(history) # 訓練の履歴を表示

  # Plot loss values
  plt.plot(history.history['loss']) # 訓練でーだの損失の推移を描画
  plt.plot(history.history['val_loss']) # バリデーションデータの損失の推移を描画
  plt.title('Model loss') # グラフのタイトル
  plt.ylabel('Loss') # y軸のラベルを設定
  plt.xlabel('Epoch') # X軸のラベルを設定
  plt.legend(['Train', 'Test'], loc='upper left') # 凡例を追加
  plt.show() # グラフを表示
  fig.savefig(LOSS_HISTORY_FILE_NAME) # グラフを指定されたファイル名で保存

  # Save model image
  plot_model(model, to_file=MODEL_IMAGE_FILE_NAME) # モデルの構造を画像ファイルに保存。'plot_model'関数は、与えられたモデルのアーキテクチャを可視化するのに使用

  encoder = Encoder.load(enc_arch, model_path) # 保存したエンコーダモデルを読み込む。
  decoder = Decoder.load(dec_arch, model_path) # 保存したデコーダモデルを読み込む
  api = InferenceAPIforAttention(encoder, decoder, vowels_vocab, lyrics_vocab) # 推論を行う為のAPIを作成。このAPIには、エンコーダ、デコーダ、および語彙が渡される

  texts = sorted(set(vowels_lst[:50]), key=len) # 'vowel_lst'から最初の50個のテキストを抽出し、文字列の長さでソート。重複したテキストは1つにまとめられる。
  for text in texts: # テキストのリストをループで処理
    decoded = api.predict(text=text) # 'api'を使用して、与えられたテキストをデコード
    print('Vowels : {}'.format(text)) # 元のテキスト(母音の部分)を表示
    print('Lyrics: {}'.format(decoded)) # デコードされた歌詞を表示

if __name__ == '__main__':
  main()
