ARTIST_NAME = "Kenshi Yonezu" # 文字列定数で、アーティストの名前
TRACKS_FILE_NAME = "Kenshi-Yonezu-tracks.csv" # 文字列定数で、アーティストの楽曲の情報が格納されるCSVファイルのファイル名
WAKATI_FILE_NAME = "Kenshi-Yonezu-wakati.csv" # 文字列定数で、アーティストの楽曲の分かち書き情報が格納されるCSVファイルのファイル名

ACC_HISTORY_FILE_NAME = "acc.png" # 文字列定数で、モデルの訓練精度の履歴グラフを保存するためのファイル名
LOSS_HISTORY_FILE_NAME = "loss.png" # 文字列定数で、モデルの訓練損失の履歴グラフを保存するためのファイル名
MODEL_IMAGE_FILE_NAME = "model.png" # 文字列定数で、モデルの画像を保存するためのファイル名

BOS = '<bos>' # 文字列定数で、「Beginning of Sentence（文の始まり）」を表す特殊なトークン
EOS = '<eos>' # 文字列定数で、「End of Sentence（文の終わり）」を表す特殊なトークン
UNK = '<unk>' # 文字列定数で、「Unknown（未知の）」を表す特殊なトークン

N_GRAM_NUMBER = 3 # 整数定数で、N-gramモデルなどで使用されるNの値

"""
これらの定数は、プロジェクト内で一貫した設定やファイル名の使用を容易にするために利用される
例えば、モデル訓練中に精度と損失の履歴をグラフで保存するときに、ファイル名を変更する必要がなくなる
"""
