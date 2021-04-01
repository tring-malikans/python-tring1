import os
# import asyncio
from binance.client import Client
from binance.websockets import BinanceSocketManager
# from twisted.internet import reactor
import pymongo
import time
# from multiprocessing import Pool
# import multiprocessing
import threading
import io
import datetime



mongo1=pymongo.MongoClient('mongodb+srv://sufiyan:sufiyan1@tring1.vef4g.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')


db = mongo1['test-database']
# # coins=["BTC","SUSHI","DOGE",'ADA','EOS','XRP','VET','TRX','LINK','THETA']
# coins=["BTC","XRP","DOGE",'ADA','THETA','']

coins=["BTC","XRP","DOGE"]
pairs=["BUSD"]





client = Client("gyHLoFuT1VKWwtWM8djg7lshfeHGkiADh6lkPsma0HBHIYAhqqZe2grzK7ZIywT0", "AUZge7ylUu48BSTONuEv8zOsWcFiHOX6hli2pHMWVQI3BHSyAii9hBiLzHzUApr3")
bm = BinanceSocketManager(client)
bm.start()


def process_messageC(msg):
    information=db["coins"]
    Event_type=msg['e']
    s = msg['E'] / 1000
    year=datetime.datetime.fromtimestamp(s).strftime('%Y')[-2:]
    Event_time=datetime.datetime.fromtimestamp(s).strftime(f'%a %m-%d-{year} %H:%M:%S.%f')[:-3]
    Event_times=msg['E']
    Symbol=msg['s']
    Aggregate_trade_ID=msg['a']
    Price=msg['p']
    Quantity=msg['q']
    if msg['m']:
        tradeType="Sell"
    else:
        tradeType="Buy"
    scrape_data=str(Event_type)+','+str(Event_time)+','+str(Event_times)+','+str(Symbol)+','+str(Aggregate_trade_ID)+','+str(Price)+','+str(Quantity)+','+str(tradeType)
    # with io.open('coins.csv','a',encoding="utf8") as f2:
    #     f2.write(scrape_data+'\n')
    #     f2.close()
    record={
        "Event_type":Event_type,
        "Event_time":Event_time,
        "Event_times":Event_times,
        "Symbol":Symbol,
        "Aggregate_trade_ID":Aggregate_trade_ID,
        "Price":Price,
        "Quantity":Quantity,
        "tradeType":tradeType
    }
    information.insert_one(record)

def process_messageT(msg):
    information=db["trades"]
    print("message type: {}".format(msg['e']))
    Event_type=msg['e']
    s = msg['E'] / 1000
    Event_time=datetime.datetime.fromtimestamp(s).strftime('%a %b %d %Y %H:%M:%S:%MS')
    Symbol=msg['s']
    Trade_ID=msg['a']
    Price=msg['p']
    Quantity=msg['q']
    scrape_data=str(Event_type)+','+str(Event_time)+','+str(Symbol)+','+str(Trade_ID)+','+str(Price)+','+str(Quantity)
    # with io.open('trades.csv','a',encoding="utf8") as f2:
    #     f2.write(scrape_data+'\n')
    #     f2.close()
    record={
        "Event_type":Event_type,
        "Event_time":Event_time,
        "Symbol":Symbol,
        "Trade_ID":Trade_ID,
        "Price":Price,
        "Quantity":Quantity
    }
    information.insert_one(record)


def start_extract_coins(coin):   
    print(coin,'xx') 
    # conn_key = bm.start_multiplex_socket(['bnbbtc@aggTrade', 'neobtc@ticker'], process_m_message)
    # time.sleep(1)
    trades = bm.start_trade_socket(coin, process_messageT)
    prices= bm.start_aggtrade_socket(coin, process_messageC)
    

process=[]
# print(bm)
# import requests\
def main():
    # for proxie in proxies:
    print("222")
    for coin in coins:
        for pair in pairs:
            newCoin=coin+pair
            process.append(newCoin)


if __name__ == '__main__':
    # application.run(host="0.0.0.0",port=8080)
    # application.run(debug=true)
    main()
    print("1")
    threads = [ threading.Thread(target = start_extract_coins, args=(p,)) for p in process ]
    [ t.start() for t in threads ]
    [ t.join() for t in threads ]