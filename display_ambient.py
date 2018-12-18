#!/usr/bin/python3.5
# coding: utf-8
################################################################################
# Rapberry Pi用 サンプルスクリプト：Apple PiのLCDとLEDへAmbientの状態を表示する
#
# 準備：
# ・Ambientキーを(https://ambidata.io)で取得し、ambient_chidとambient_rkeyへ入力
# ・表示したいAmbientのデータ番号（d1～d8）のいずれかをamdient_tagへ入力
#
#                                          Copyright (c) 2018-2019 Wataru KUNINO
################################################################################

import json
import urllib.request
import datetime
from time import sleep

ambient_chid='0000'                 # ここにAmbientで取得したチャネルIDを入力
ambient_rkey='0123456789abcdef'     # リードキーを入力 ※ライトキーではない
amdient_tag='d1'                    # データ番号d1～d8のいずれかを入力

while True:
    url  = 'https://ambidata.io/api/v2/channels/'+ambient_chid+'/data\?readKey='+ambient_rkey+'\&n=1'
    post = urllib.request.Request(url)
    res  = urllib.request.urlopen(post)
    if res:
        payl = json.loads(res.read().decode())
    #   print('Response:', payl)
        if amdient_tag in payl[0]:
            val = payl[0][amdient_tag]
            date= payl[0]['created']
            date = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%fZ")
            date += datetime.timedelta(hours=9)
            print(date.strftime('%Y/%m/%d %H:%M'), end='')  # 日付出力(改行無し)
            print(',',val)                                  # 受信データを出力
    sleep(20)
