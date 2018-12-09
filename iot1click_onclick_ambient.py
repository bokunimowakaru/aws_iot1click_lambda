# for AWS Lambda Python 3.6
# coding: utf-8
################################################################################
# SORACOM LTE-Button や AWS IoT Buttonが押された時にAmbient へボタン値を送信する
#
# 準備：
# ・IoT 1-Clickのデバイス登録、プロジェクト作成（ロール設定、Lambda関数設定）
# ・Ambientキーを(https://ambidata.io)で取得し、ambient_chidとambient_wkeyへ入力
# ・Ambientのデータ番号（d1～d8）のいずれかをamdient_tagへ入力
#
#                                          Copyright (c) 2018-2019 Wataru KUNINO
################################################################################

import json
import urllib.request
ambient_chid='0000'                 # ここにAmbientで取得したチャネルIDを入力
ambient_wkey='0123456789abcdef'     # ここにはライトキーを入力
amdient_tag='d1'                    # データ番号d1～d8のいずれかを入力

def lambda_handler(event, context):
    # AWS IoT 1-Clickから受け取ったデバイスIDとクリック方法を変数dsnとbtnへ代入
    print('Received event: ' + json.dumps(event))
    dsn  = event['deviceInfo']['deviceId']
    btn  = event['deviceEvent']['buttonClicked']['clickType']
    
    # クリック方法typeに応じて変数type_numに0～2の値を設定
    type_num=0
    if btn == 'SINGLE':
        type_num=1
    elif btn == 'DOUBLE':
        type_num=2
    elif btn == 'LONG':
        type_num=0
    
    # ボタン取得結果のログ出力
    print('btn: type=',type_num,'(',btn,')')
    
    # Ambientへ送信
    url  = 'https://ambidata.io/api/v2/channels/'+ambient_chid+'/data'
    head = {"Content-Type":"application/json"}
    body = {"writeKey" : ambient_wkey, amdient_tag : type_num}
    print(body)
    post = urllib.request.Request(url, json.dumps(body).encode(), head)
    res  = urllib.request.urlopen(post)
    if res:
        print('Response:', res.read())
        return 'Done'
