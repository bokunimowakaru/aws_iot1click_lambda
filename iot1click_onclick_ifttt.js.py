# coding: utf-8
################################################################################
# SORACOM LTE-Button �� AWS IoT Button�������ꂽ�Ƃ���IFTTT �փg���K�𑗐M����
#
# �����F
# IFTTT��Key��(https://ifttt.com/maker_webhooks)�Ŏ擾���A�ϐ�ifttt_token�֑��
#
#                                          Copyright (c) 2018-2019 Wataru KUNINO
################################################################################

import json
import urllib.request
import datetime

ifttt_token='IFTTT��Webhocks�Ŏ擾����Token���L������'
ifttt_event='notify'
msg='�{�^����������܂���'

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
