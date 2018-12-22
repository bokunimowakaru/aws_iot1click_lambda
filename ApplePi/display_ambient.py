#!/usr/bin/python3
# coding: utf-8
################################################################################
# Apple PiのLCDとLEDへAmbientの状態を表示する
#
# 準備：
# AmbientのKeyを(https://ambidata.io)で取得し、ambient_chidとambient_rkeyへ代入
#
#                                          Copyright (c) 2018-2019 Wataru KUNINO
################################################################################

import json
import urllib.request
import datetime
from time import sleep
import ApplePi.initLCD
import ApplePi.onLED1
import ApplePi.onLED2
import ApplePi.offLED1
import ApplePi.offLED2
import subprocess

ambient_chid='0000'                 # ここにAmbientで取得したチャネルIDを入力
ambient_rkey='0123456789abcdef'     # リードキーを入力 ※ライトキーではない
amdient_tag='d1'                    # データ番号d1～d8のいずれかを入力

ap_locate='ApplePi/locateLCD.py'
ap_print='ApplePi/printLCD.py'
ap_led1=['ApplePi/offLED1.py','ApplePi/onLED1.py']
ap_led2=['ApplePi/offLED2.py','ApplePi/onLED2.py']
while True:
    url  = 'https://ambidata.io/api/v2/channels/'+ambient_chid+'/data\?readKey='+ambient_rkey+'&n=1'
    post = urllib.request.Request(url)
    res  = urllib.request.urlopen(post)
    if res:
        payl = json.loads(res.read().decode())
    #   print('Response:', payl)
        if amdient_tag in payl[0]:
            val = int(payl[0][amdient_tag])
            date= payl[0]['created']
            date = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%fZ")
            date += datetime.timedelta(hours=9)
            print(date.strftime('%Y/%m/%d %H:%M'), end='')  # 日付を出力
            print(',',val)                                  # 受信データを出力
            
            # ApplePiへの表示・出力
            subprocess.call([ap_locate,'0','0'])
            subprocess.call([ap_print,date.strftime('%Y/%m/%d')[2:]])
            subprocess.call([ap_locate,'0','1'])
            subprocess.call([ap_print,date.strftime('%H:%M')])
            subprocess.call([ap_locate,'7','1'])
            subprocess.call([ap_print,str(val)])
            if val <= 0:
                subprocess.call([ap_led1[0]])
                subprocess.call([ap_led2[0]])
            elif val == 1:
                subprocess.call([ap_led1[0]])
                subprocess.call([ap_led2[1]])
            elif val >= 2:
                subprocess.call([ap_led1[1]])
                subprocess.call([ap_led2[1]])
    sleep(20)
