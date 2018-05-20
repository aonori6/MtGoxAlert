#_*_ coding: utf-8 _*_

import urllib3
import json
import pandas as pd
import time
import twitter
import logging

def setupLogging():
    logging.basicConfig(
        level=logging.INFO,
        format = '%(asctime)s %(levelname)s: %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S')
    logging.getLogger('')
    logging.info('Start logging...')

def sat2btc(a):
    return a/100000000

def tweet(message):
    with open('.apisecret.json', 'r') as f:
        loaddata = json.load(f)
    consumer_key = loaddata["consumer_key"]
    consumer_secret = loaddata["consumer_secret"]
    token = loaddata["token"]
    token_secret = loaddata["token_secret"]
    auth = twitter.OAuth(consumer_key=consumer_key, consumer_secret=consumer_secret, token=token, token_secret=token_secret)

    try:
        tw = twitter.Twitter(auth=auth)
        tw.statuses.update(status=message)
        logging.info('Tweet!!')
    except:
        logging.error('Could not tweet...')

def line(message):
    with open('.apisecret.json', 'r') as f:
        loaddata = json.load(f)
    line_token = loaddata["line_token"]
    payload = {"message": message}
    headers = {"Authorization": "Bearer " + line_token}
    url = 'https://notify-api.line.me/api/notify'
    try:
        http.request('POST', url, fields=payload, headers=headers)
        logging.info('Line!!')
    except:
        logging.error('Could not notify...')

if __name__ == '__main__':
    setupLogging()

    with open('MtGoxColdWalletAddress.json', 'r') as f:
        loaddata = json.load(f)
    address_list = loaddata["address"]

    cols = ["hash160", "address", "n_tx", "total_received", "total_sent", "final_balance"]
    df = pd.DataFrame(index=[], columns=cols)

    http = urllib3.PoolManager()
    # Suppress error messages regarding to SSL certification(s)
    from urllib3.exceptions import InsecureRequestWarning
    urllib3.disable_warnings(InsecureRequestWarning)

    urlhead = 'https://blockchain.info/ja/rawaddr/'
    for i in range(len(address_list)):
        url = urlhead + address_list[i]
        while True:
            try:
                response = json.loads(http.request('GET', url).data.decode('utf-8'))
                break
            except:
                logging.error('API request failed...')
                time.sleep(1)
        hash160 = response["hash160"]
        address = response["address"]
        n_tx = response["n_tx"]
        total_received = response["total_received"]
        total_sent = response["total_sent"]
        final_balance = response["final_balance"]

        series = pd.Series([hash160, address, n_tx, total_received, total_sent, final_balance], index=cols)
        df = df.append(series, ignore_index = True)

        time.sleep(1)

    logging.info('Initial data set is obtained...')

    while True:
        for i in range(len(df.index)):
            url = urlhead + df["address"][i]
            while True:
                try:
                    response = json.loads(http.request('GET', url).data.decode('utf-8'))
                    break
                except:
                    logging.error('API request failed...')
                    time.sleep(1)
            if response["n_tx"] != df["n_tx"][i]:
                logging.info('New transaction is detected...')
                diff = df["final_balance"][i] - response["final_balance"]
                message = str(sat2btc(diff)) + " BTC is moved from Mt Gox address:" + df["address"][i]
                # tweet(message)
                line(message)
                df["n_tx"][i] = response["n_tx"]
                df["total_received"][i] = response["n_tx"]
                df["total_sent"][i] = response["total_sent"]
                df["final_balance"][i] = response["final_balance"]

            time.sleep(1)
