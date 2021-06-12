import pandas as pd
import datetime
import requests
import time
import os
import hashlib
import json

def downloadIntraday(fromSymbol, toSymbol, fromDate, toDate, minutesAggregate=1, cache=True, cacheDir='_cache'):
        print('Downloading %s->%s pair price...' % (fromSymbol, toSymbol))

        df = pd.DataFrame()

        if toDate <= 0:
                toDate = int(time.time()) 

        if fromDate <=0:
                fromDate = toDate

        untilt = toDate
        pending = True

        while pending:
                url = 'https://min-api.cryptocompare.com/data/v2/histominute' + \
                        '?tryConversion=false' + \
                        '&limit=2000' + \
                        '&fsym=' + fromSymbol + \
                        '&tsym=' + toSymbol + \
                        '&toTs=' + str(untilt) + \
                        '&aggregate=' + str(minutesAggregate)

                hash_object = hashlib.md5(url.encode())
                hs = hash_object.hexdigest()
                cache_file = cacheDir + '/crypcomp-' + fromSymbol.lower() + '-' + toSymbol.lower() + '-' + str(untilt) + '-' + str(minutesAggregate) + '-' + hs + '.json'

                jsondata = ''
                if cache and os.path.isfile(cache_file):
                        print('Reusing cached results')
                        jsondata = loadJSONFile(cache_file)
                        os.system("touch -c %s" % cache_file)

                else:
                        print('Downloading data from ' + url + '...')
                        response = requests.get(url)
                        jsondata = response.json()

                        if cache:
                                saveFile(cache_file, response.text)

                try:
                        data = jsondata['Data']['Data']
                except:
                        print('Error parsing data')
                        raise

                df1 = pd.DataFrame(data)
                untilt = df1.time[0]
                pending = untilt > fromDate
                df1 = df1[:-1]

                df = df.append(df1)

        df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]

        df = df.rename(columns={"timestamp": "date", "open": "open", "high": "high", "low": "low", "close": "close", "volumefrom": "volume"})
        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        df.set_index('date', inplace=True)
        df.sort_index(inplace=True)

        print('Download complete. count=' + str(len(df)))
        return df

def loadJSONFile(filename):
    with open(filename, 'r') as fr:
        return json.load(fr)

def saveFile(filename, contents):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'w') as fw:
        fw.write(contents)
        fw.flush()
