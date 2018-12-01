# for AWS Lambda Python 3.6
# coding: utf-8
################################################################################
# SORACOM LTE-Button や AWS IoT Buttonが押された時にAmbient へボタン値を送信する
#
# 準備：
# AmbientのKeyを(https://ambidata.io)で取得し、ambient_chidとambient_wkeyへ代入
#
#                                          Copyright (c) 2018-2019 Wataru KUNINO
################################################################################

import json
import urllib.request
ambient_chid='725'                  # ここにAmbientで取得したチャネルIDを入力
ambient_wkey='26ee8c088f61194d'     # リードキーを入力 ※ライトキーではない
amdient_tag='d3'                    # データ番号d1～d8のいずれかを入力

def lambda_handler(event, context):
    print('Received event: ' + json.dumps(event))
    dsn  = event['deviceInfo']['deviceId']
    btn  = event['deviceEvent']['buttonClicked']['clickType']
    num=0
    if btn == 'SINGLE':
        num=1
    elif btn == 'DOUBLE':
        num=2
    elif btn == 'LONG':
        num=0
    print('btn=',num)
    url  = 'https://ambidata.io/api/v2/channels/'+ambient_chid+'/data'
    head = {"Content-Type":"application/json"}
    body = {"writeKey":ambient_wkey, amdient_tag:num}
    print(body)
    post = urllib.request.Request(url, json.dumps(body).encode(), head)
    res  = urllib.request.urlopen(post)
    if res:
        print('Response:', res.read())
        return 'Done'
