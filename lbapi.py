#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import hmac
import requests
from time           import time
from urllib   import urlencode
import ConfigParser

params_template_buy = {
   'price_equation': 'bitfinexusd*USD_in_RUB*0.5', 
   'lat': '1', 
   'lon': '2', 
   'city': 'Moscow', 
   'location_string': 'Moscow, Russia', 
   'countrycode': 'RU', 
   'currency': 'RUB', 
   'account_info': 'Nothing', 
   'bank_name': 'Альфабанк', 
   'msg': '''1. Укажите нужную сумму и начните сделку.
2. Мои биткойны задепонируются (заблокируются), и мне придет сообщение о новой транзакции. 
3. Я выйду на связь с вами посредством системы сообщений на LocalBitcoins и подтвержу, что все готово к принятию Вашего платежа.
4. Я предоставлю Вам номер карты, и вы сделаете платеж. В комментариях к Вашему платежу укажите просто "Мат. помощь". 
5. Сразу после получения платежа я разблокирую Ваши биткойны и они окажутся у Вас.''', 
   'sms_verification_required': 'yes', 
   'track_max_amount': '0', 
   'require_trusted_by_advertiser': 'yes', 
   'require_identification': 'yes',
   'trade_type': 'ONLINE_BUY',
   'online_provider': 'SPECIFIC_BANK',
   'min_amount': 200,
   'max_amount': 4000
}

params_template_sell = {
   'price_equation': 'bitfinexusd*USD_in_RUB*1.5', 
   'lat': '1', 
   'lon': '2', 
   'city': 'Moscow', 
   'location_string': 'Moscow, Russia', 
   'countrycode': 'RU', 
   'currency': 'RUB', 
   'account_info': 'Nothing', 
   'bank_name': 'Альфабанк', 
   'msg': 'Test message', 
   'sms_verification_required': 'yes', 
   'track_max_amount': '0', 
   'require_trusted_by_advertiser': 'yes', 
   'require_identification': 'yes',
   'trade_type': 'ONLINE_SELL',
   'online_provider': 'SPECIFIC_BANK',
   'min_amount': 200,
   'max_amount': 4000
}

def getParam(path, section, param):
     config = ConfigParser.ConfigParser()
     config.readfp(open(path))
     return config.get( section, param)

def makeRequest(path, params, method):
    key = getParam('cred.conf','localbitcoins','lb_key')
    secret = getParam('cred.conf','localbitcoins','lb_secret')
    nonce   = str(int(time()))
    paramsEncoded = urlencode(params)
    message = nonce + key + path + paramsEncoded
    signature = hmac.new(secret.encode('utf-8'), msg=message.encode('utf-8'), digestmod=hashlib.sha256).hexdigest().upper()
    headers = {
        'Apiauth-Key'       : key,
        'Apiauth-Nonce'     : nonce,
        'Apiauth-Signature' : signature
    }
    if method == 'get':
        req = requests.get('https://localbitcoins.com' + path, headers=headers, params=params)
    elif method == 'post':
        req = requests.post('https://localbitcoins.com' + path, headers=headers, data=params)
    data = req.json()
    print(data)
    return data

def makePublicRequest(path, params, method):
    if method == 'get':
        req = requests.get('https://localbitcoins.com' + path)
    elif method == 'post':
        req = requests.post('https://localbitcoins.com' + path)
    data = req.json()
    return data

def getTopAds(count,sellbuy):
# sellbuy = 'sell' or 'buy'
# SPECIFIC_BANK
    payment_method = 'transfers-with-specific-bank'
    top = []
    data = makePublicRequest('/%s-bitcoins-online/ru/russia/%s/.json' % (sellbuy,payment_method),{},'get')
    for i in range(0,count):
        info = [
            data['data']['ad_list'][i]['data']['ad_id'],
            data['data']['ad_list'][i]['data']['temp_price'],
            data['data']['ad_list'][i]['data']['profile']['username'],
        ]
        top.append(info)
    return top 

def BestPrice(pos,sellbuy):
    # will not work for pos = 1 !!!!
    top = getTopAds(pos,sellbuy)
    print top
    left = float(top[pos-2][1])
    right = float(top[pos-1][1])
    delta = round(abs(left - right)/2)
    if sellbuy == 'sell':
       bestprice = left - delta 
    elif sellbuy == 'buy':
       bestprice = right - delta 
    return bestprice


def publishAds(trade_type, price):
    if trade_type == 'ONLINE_BUY':
        params = params_template_buy
    elif trade_type== 'ONLINE_SELL':
        params = params_template_sell
    else:
        return 1
    params['price_equation'] = price
    data = makeRequest('/api/ad-create/', params, 'post')
    return data

def main():
     params = params_template     
     makeRequest('/api/ad-create/', params, 'post')


if __name__ == "__main__":
    main()

