This is a simple project I threw together to allow quick interactions with Cryptowat.ch's public REST API via python.

The JSON responses from Cryptowat.ch are converted into python objects to simplify interactions. For example...

```python
import cryptowatch.Client as cl
import matplotlib.pyplot as plt
import numpy as np

#print a list of available markets on coinbase
for x in cl.GetMarkets("coinbase"):
    print x

#create a client which targets Coinbase's ETH-USD market
client = cl.MarketClient("coinbase", "ethusd")

#create a time plot of recent ETH-USD trades
trades = client.GetTrades()
plt.figure()
plt.plot(*zip(*[(x.timestamp, x.price) for x in trades]))
plt.show()

#etc, etc

#plot the current order book

order_book = client.GetOrderBook()

bid_prices = [x.price for x in order_book.bids]
bid_sizes = np.cumsum([x.size for x in order_book.bids])
ask_prices = [x.price for x in order_book.asks if x.price < 150]
ask_sizes = np.cumsum([x.size for x in order_book.asks if x.price < 150])

plt.figure()
ax = plt.gca()

plt.plot(bid_prices, bid_sizes, lw=1, color='green')
ax.fill_between(bid_prices, bid_sizes, interpolate=False, color='green')
plt.plot(ask_prices, ask_sizes, lw=1, color='red')
ax.fill_between(ask_prices, ask_sizes, interpolate=True, color='red')
plt.show()
```

I am in no way affiliated with Cryptowat.ch.
