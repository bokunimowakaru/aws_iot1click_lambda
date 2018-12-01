# coding: utf-8
################################################################################
# SORACOM LTE-Button や AWS IoT Buttonが押されたときにIFTTT へトリガを送信する
#
# 準備：
# IFTTTのKeyを(https://ifttt.com/maker_webhooks)で取得し、変数ifttt_tokenへ代入
#
#                                          Copyright (c) 2018-2019 Wataru KUNINO
################################################################################

import json
import urllib.request
import datetime

ifttt_token='IFTTTのWebhocksで取得したTokenを記入する'
ifttt_event='notify'
msg='ボタンが押されました'

def lambda_handler(event, context):
    print('Received event: ' + json.dumps(event))
    dsn  = event['deviceInfo']['deviceId']
    btn  = event['deviceEvent']['buttonClicked']['clickType']
    date = event['deviceEvent']['buttonClicked']['reportedTime']
    date = datetime.datetime.strptime(date,"%Y-%m-%dT%H:%M:%S.%fZ")
    date += datetime.timedelta(hours=9)
    url  = 'https://maker.ifttt.com/trigger/'+ifttt_event+'/with/key/'+ifttt_token
    head = {"Content-Type":"application/json"}
    body = {"value1":'{}({}, {}, {})'.format(msg,date.strftime('%Y/%m/%d %H:%M'),dsn,btn)}
    print(body)
    post = urllib.request.Request(url, json.dumps(body).encode(), head)
    result = urllib.request.urlopen(post)
    if result:
        print('Result:', result.read())
        return 'Done'
