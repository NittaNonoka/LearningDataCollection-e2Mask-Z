# e2Mask-Zの学習データ収集プログラム

マスクの学習データを表情ごとに一つ一つ収集できるプログラム。


# DEMO

```bash
python learning.py

Please enter a learning number
{0:ニュートラル 1:喜び 2:怒り　3:驚き　4:悲しみ} 
収集したい表情の番号を入力[Enter]
センサーデータ
...

```

<img width="651" alt="image" src="https://user-images.githubusercontent.com/40416853/99477959-e93f3900-2996-11eb-9dba-6669c0640516.png">

収集したデータは自動的にcsvファイルに追記されます。

csvファイルの一番左の列にはラベルが入ります。{0:ニュートラル 1:喜び 2:怒り　3:驚き　4:悲しみ} 

# Features
各表情のセンサーデータを収集
個々に実行が可能

# Requirement

必要な環境

* Python3系
* Arduino IDE


# Usage

実行方法

自分のPCにクローンして、実行する

Arduinoを繋ぐCOMポートの名称は適宜変えてください
```bash
git clone https://github.com/NittaNonoka/e2MaskViewer.git
python learning.py
```

# Note
masterブランチにはPushしないこと！
