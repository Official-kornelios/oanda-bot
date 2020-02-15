#import relevant packages and modules
import json
import sys
import time
import datetime
from datetime import datetime as dt
from datetime import timedelta
import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments


#configure account detals
api = API(access_token="73f0ccf276442f7a4e6d155fea2557c9-0e570792a909c2e34946221b22aa551a")
accountID = "101-001-13441045-001"

#configure params for api calls
instrument_params = {
    "instrument": "EUR_USD",
    "granularity": "H6",
    "from": "2019-12-01",
    "to": "2019-12-13",
    "smooth": False,
}

candles_params = {
    "granularity": "H6",
    "from": "2020-02-01",
    "to": "2020-02-11",
    "pricingComponent":"M",
}

#other possible options are GBP_ZAR, NZD_SGD, USD_HKD, GBP_PLN, USD_JPY, USD_CNH, SGD_HKD
#EUR_HUF, AUD_NZD, CAD_JPY, ZAR_JPY, EUR_AUD, HKD_JPY, USD_NOK, USD_CZK, CAD_SGD
pair = "EUR_USD"

## Parses a granularity like S10 or M15 into the corresponding number of seconds
## Does not take into account anything weird, leap years, DST, etc.
is_dst = time.daylight and time.localtime().tm_isdst > 0
utc_offset = (time.altzone if is_dst else time.timezone)
def getGranularitySeconds(granularity):
    if granularity[0] == 'S':
        return int(granularity[1:])
    elif granularity[0] == 'M' and len(granularity) > 1:
        return 60*int(granularity[1:])
    elif granularity[0] == 'H':
        return 60*60*int(granularity[1:])
    elif granularity[0] == 'D':
        return 60*60*24
    elif granularity[0] == 'W':
        return 60*60*24*7
    #Does not take into account actual month length
    elif granularity[0] == 'M':
        return 60*60*24*30


def SMA(period):
    period = int(period)
    datetimeFormat = '%Y-%m-%d %H:%M:%S.%f' 
    date1 = dt.now()
    diff = timedelta(days = int(period))
    date2 = (date1 - diff)
    from_date = datetime.datetime.strptime(str(date2), datetimeFormat).strftime("%Y-%m-%d")
    to_date = datetime.datetime.strptime(str(date1), datetimeFormat).strftime("%Y-%m-%d")
    params = {}
    params['granularity'] = "H6"
    params['from'] = from_date
    params['to'] = to_date
    r = instruments.InstrumentsCandles(
        instrument=pair,
        params=params
    )
    api.request(r)
    response = r.response
    candles = response['candles']
    candlewidth = getGranularitySeconds("D")
    now = time.time() + utc_offset
    finalsma = 0
    count = 0
    oldest = now - (period * candlewidth)
    oldprice = 0
    for candle in candles:
        candleTime = time.mktime(time.strptime(str(candle['time']),  '%Y-%m-%dT%H:%M:%S.%f000Z'))
        if candleTime < oldest:
            oldprice = candle['mid']['c']
            continue
        else:
            while oldest < candleTime:
                finalsma += float(oldprice)
                count += 1
                oldest += candlewidth
            oldprice = candle['mid']['c']
        
    while oldest < now:
        raw_sma = candles[-1]['mid']['c']
        new_sma = float(raw_sma)
        finalsma += new_sma
        count += 1
        oldest += candlewidth
    SMA = float(finalsma)/float(period)
    # print ("SMA:", SMA)
    return (SMA)

def logic():
    if SMA(20) < SMA(100):
        #short or sell
        data = {}
        data['units'] = -10
        data['instrument'] = pair
        data['timeInForce'] = "FOK"
        data['type'] = "MARKET"
        print('sell')
        return (data)

    elif SMA(20) > SMA(100):
        #long or buy
        data = {}
        data['units'] = 10
        data['instrument'] = pair
        data['timeInForce'] = "FOK"
        data['type'] = "MARKET"
        print('buy')
        return(data)

if __name__ == "__main__":
    logic()