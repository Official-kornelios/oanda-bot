import oandapyV20
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders

#configure account detals
api = API(access_token="73f0ccf276442f7a4e6d155fea2557c9-0e570792a909c2e34946221b22aa551a")
accountID = "101-001-13441045-001"

def cancel(accountID, orderID):
    r = orders.OrderCancel(accountID, orderID)
    api.request(r)
    print (r.response)
    return (r.response)

if __name__ == "__main__":
    cancel("101-001-13441045-001", "200002")