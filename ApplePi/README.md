# Apple Pi の使い方

![Apple Pi 接続例](ApplePi.jpg)

## ステップ1

* Raspberry Piの設定ツールを起動する
	sudo raspi-config
* I2Cの有効化 [5]→[P5]

## ステップ2

* i2c-toolsをインストールする（不要かも）
	sudo apt-get install i2c-tools

## ステップ3

* CQ出版社のサイトからApplePi専用ライブラリをダウンロードして展開する

	wget https://toragi.cqpub.co.jp/Portals/0/support/2016/201608ApplePi/ApplePi.tar
	tar xvf ApplePi.tar

* 必要ファイルとフォルダ（ディレクトリ）構成は以下のようになる

	aws_iot1click_lambda  
	├── ApplePi  
	│   ├── display_ambient.py  
	│   └── ApplePi  
	│        ├── initLCD.py  
	│        ├── locateLCD.py  
	│        ├── offLED1.py  
	│        ├── offLED2.py  
	│        ├── onLED1.py  
	│        ├── onLED2.py  
	│        └── printLCD.py  
	└── display_ambient.py (ApplePi 不要)  

## 参考文献
* トラ技2016年8月号 P.129
* ビットレードワン  
http://bit-trade-one.co.jp/product/module/adcq1608p/
