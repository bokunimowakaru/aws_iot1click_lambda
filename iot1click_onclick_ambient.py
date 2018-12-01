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
ambient_chid='725'
ambient_wkey='ad3e53b54fe16764'
amdient_tag='d5'

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
        num=3
    print('btn=',num)
    url  = 'https://ambidata.io/api/v2/channels/'+ambient_chid+'/data'
    head = {"Content-Type":"application/json"}
    body = {"writeKey":ambient_wkey, amdient_tag:num}
    print(body)
    post = urllib.request.Request(url, json.dumps(body).encode(), head)
    result = urllib.request.urlopen(post)
    if result:
        print('Result:', result.read())
        return 'Done'
