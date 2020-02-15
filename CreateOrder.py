import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
from bot import logic

#configure account detals
api = API(access_token="73f0ccf276442f7a4e6d155fea2557c9-0e570792a909c2e34946221b22aa551a")
accountID = "101-001-13441045-001"

##different data parameters for order data
##create market order to BUY 100 units
# {
#   "order": {
#     "units": "100",
#     "instrument": "EUR_USD",
#     "timeInForce": "FOK",
#     "type": "MARKET",
#     "positionFill": "DEFAULT"
#   }
# }

##create market order to SELL 100 units
# {
#   "order": {
#     "units": "-100",
#     "instrument": "EUR_USD",
#     "timeInForce": "FOK",
#     "type": "MARKET",
#     "positionFill": "DEFAULT"
#   }
# }

##curl: Create a Take Profit Order @ 1.6000 for Trade with ID 6368
# {
#   "order": {
#     "timeInForce": "GTC",
#     "price": "1.6000",
#     "type": "TAKE_PROFIT",
#     "tradeID": "6368"
#   }
# }

##curl: Create a Limit Order for -1000 USD_CAD @ 1.5000 with a Stop Loss on Fill @ 1.7000 and a Take Profit @ 1.14530
# {
#   "order": {
#     "price": "1.5000",
#     "stopLossOnFill": {
#       "timeInForce": "GTC",
#       "price": "1.7000"
#     },
#     "takeProfitOnFill": {
#       "price": "1.14530"
#     },
#     "timeInForce": "GTC",
#     "instrument": "USD_CAD",
#     "units": "-1000",
#     "type": "LIMIT",
#     "positionFill": "DEFAULT"
#   }
# }

#define params for order
def create(accountID, data):
    r = orders.OrderCreate(accountID, data=data)
    api.request(r)
    print (r.response)
    return (r.response)

def botOrder(accountID, data):
    r = orders.OrderCreate(accountID, data=data)
    api.request(r)
    # print (r.response)
    return (r.response)

def listOrder():
    r = orders.OrderList(accountID)
    api.request(r)
    print(r.response)

def listTrades():
    r = trades.OpenTrades(accountID)
    api.request(r)
    print(r.response)

##importing logic for making orders
data = {}
data['order'] = logic()

if __name__ == "__main__":
    # data = {
    #     "order": {
    #         "units": "1",
    #         "instrument": "EUR_USD",
    #         "timeInForce": "FOK",
    #         "type": "MARKET",
    #         "positionFill": "DEFAULT"
    #     }
    # }
    # create("101-001-13441045-001", data=data)

    botOrder(accountID, data = data)
    listOrder()
    listTrades()