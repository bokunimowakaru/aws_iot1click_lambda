# for AWS Lambda Python 3.6
# coding: utf-8
################################################################################
# SORACOM LTE-Button や AWS IoT Buttonが押された時にAmbient へボタン値を送信する
# 過去の押下回数を AWS のデータベースへ保存しておき、Ambientで累積押下回数を表示
#
# 準備：
# ・IoT 1-Clickのデバイス登録、プロジェクト作成（ロール設定、Lambda関数設定）
# ・Ambientキーを(https://ambidata.io)で取得し、ambient_chidとambient_wkeyへ代入
# ・Ambientのデータ番号（d4～d8）のいずれかをamdient_tagへ代入
# ・DynamoDBテーブルの作成（テーブル名=button, プライマリキー=type）
# ・IAMロール設定（使用中のLambda用ロールへDynamoDBのアクセス権を追加）
#
#                                          Copyright (c) 2018-2019 Wataru KUNINO
################################################################################

import json
import urllib.request
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

ambient_chid='0000'                 # ここにAmbientで取得したチャネルIDを入力
ambient_wkey='0123456789abcdef'     # ここにはライトキーを入力
amdient_tag='d4'                    # データ番号d4～d8のいずれかを入力

# データベース選択
db = boto3.resource('dynamodb')
dbTable = db.Table('button')

def lambda_handler(event, context):
    # AWS IoT 1-Clickから受け取ったデバイスIDとクリック方法を変数dsnとbtnへ代入
    print('Received event: ' + json.dumps(event))
    dsn  = event['deviceInfo']['deviceId']
    btn  = event['deviceEvent']['buttonClicked']['clickType']
    
    # データベースから過去の押下回数を取得
    try:
        dbVals = dbTable.query(
            KeyConditionExpression = Key('type').eq(btn)
        )
        for line in dbVals['Items']:
            print('db',line)
    except Exception as e:
        return e
    
    # 押下回数に1を加算
    try:
        count = dbVals['Items'][0]['count'] + 1
    except Exception as e:
        count = 1
        print('new type of button: ' + btn)
    
    # データベースへ押下回数を更新
    try:
        res = dbTable.update_item(
            Key = {'type': btn },
            AttributeUpdates = {
                'count':{
                    'Action': 'PUT',
                    'Value': count
                }
            }
        )
    except Exception as e:
        return e
    
    # クリック方法typeに応じて変数type_numとd_numに値を設定
    type_num=0
    d_num=4
    if btn == 'SINGLE':
        type_num=1			# クリック方法 1
        d_num=1				# Ambient データ番号 1
    elif btn == 'DOUBLE':
        type_num=2			# クリック方法 2
        d_num=2				# Ambient データ番号 2
    elif btn == 'LONG':
        type_num=0			# クリック方法 0
        d_num=3				# Ambient データ番号 3
    amdient_sum_tag='d'+str(d_num)
    
    # ボタン取得結果のログ出力
    print('btn: type=',type_num,'(',btn,'), d=',d_num, 'count=',count)
    
    # Ambientへ送信
    url  = 'https://ambidata.io/api/v2/channels/'+ambient_chid+'/data'
    head = {"Content-Type":"application/json"}
    body = {"writeKey" : ambient_wkey,
            amdient_sum_tag : int(count), amdient_tag : type_num}
    print('http:',body)
    post = urllib.request.Request(url, json.dumps(body).encode(), head)
    res = urllib.request.urlopen(post)
    if res:
        print('Response:', res.read())
        return 'Done'
