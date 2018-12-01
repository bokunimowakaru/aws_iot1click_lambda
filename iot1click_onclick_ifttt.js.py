# for AWS Lambda Python 3.6
# coding: utf-8
################################################################################
# SORACOM LTE-Button や AWS IoT Buttonが押されたときにIFTTT へトリガを送信する
#
# 準備：
# IFTTTのWebhocks(https://ifttt.com/maker_webhooks)でToken取得し、ifttt_tokenへ
#
#                                          Copyright (c) 2018-2019 Wataru KUNINO
################################################################################

import json
import urllib.request
import datetime

ifttt_token='0123456-012345678ABCDEFGHIJKLMNOPQRSTUVWXYZ'   # ここにTokenを記入
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
    body = {"value1":'{}({}, {}, {})'.format(msg,date.strftime('%Y/%m/%d %H:%M'),dsn[-4:],btn)}
    print(body)
    post = urllib.request.Request(url, json.dumps(body).encode(), head)
    res  = urllib.request.urlopen(post)
    if res:
        print('Response:', res.read())
        return 'Done'
