# for AWS Lambda Python 3.6
# coding: utf-8
################################################################################
# SORACOM LTE-Button や AWS IoT Buttonが押されたときにIFTTT へトリガを送信する
#
# 準備：
# ・IoT 1-Clickのデバイス登録、プロジェクト作成（ロール設定、Lambda関数設定）
# ・IFTTTのWebhocks(https://ifttt.com/maker_webhooks)のTokenをifttt_tokenへ入力
#
#                                          Copyright (c) 2018-2019 Wataru KUNINO
################################################################################

import json
import urllib.request
import datetime

ifttt_token='0123456-012345678ABCDEFGHIJKLMNOPQRSTUVWXYZ'   # ここにTokenを記入
ifttt_event='notify'                                        # イベント名を記入
msg='ボタンが押されました'

def lambda_handler(event, context):
    # AWS IoT 1-Clickから受け取ったデバイスIDとクリック方法などを変数へ代入
    print('Received event: ' + json.dumps(event))
    dsn  = event['deviceInfo']['deviceId']
    btn  = event['deviceEvent']['buttonClicked']['clickType']
    date = event['deviceEvent']['buttonClicked']['reportedTime']
    date = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%fZ")
    date += datetime.timedelta(hours=9)
    
    # IFTTTへ送信
    url  = 'https://maker.ifttt.com/trigger/'+ifttt_event+'/with/key/'+ifttt_token
    head = {"Content-Type":"application/json"}
    body = {"value1":'{}({}, {}, {})'.format(msg,date.strftime('%Y/%m/%d %H:%M'),dsn[-4:],btn)}
    print(body)
    post = urllib.request.Request(url, json.dumps(body).encode(), head)
    res  = urllib.request.urlopen(post)
    if res:
        print('Response:', res.read())
        return 'Done'
