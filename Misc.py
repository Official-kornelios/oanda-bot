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
    "to": "2019-12-09",
    "smooth": False,
}

candles_params = {
    "granularity": "D",
    "from": "2020-02-12",
    "to": "2020-02-15",
    "pricingComponent":"M",
}

#configure period difference
datetimeFormat = '%Y-%m-%d'
date1 = candles_params["from"]
date2 = candles_params["to"]
diff = datetime.datetime.strptime(date1, datetimeFormat)\
    - datetime.datetime.strptime(date2, datetimeFormat)


def listTrade():
    r = trades.TradesList(accountID)
    # show the endpoint as it is constructed for this call
    print("REQUEST:{}".format(r))
    rv = api.request(r)
    print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))

def listInstruments():
    r = accounts.AccountInstruments(accountID="101-001-13441045-001", params=instrument_params)
    api.request(r)
    print(r.response)
#get the account activity - Trades, Orders and Open transactions
def accountSummary():
    r = accounts.AccountSummary(accountID)
    api.request(r)
    print(r.response)

#get the forex data in the form of candlestick. kindly note other forms of data are not currently supported by Oanda API at the moment
def getCandles():
    r = instruments.InstrumentsCandles(instrument="EUR_USD",params=candles_params)
    api.request(r)
    print(r.response)
    


if __name__ == "__main__":
    listInstruments()