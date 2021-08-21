import ccxt
import rillrate
import time

kraken = ccxt.kraken()
binance = ccxt.binance()

rillrate.install()
exchanges = rillrate.Selector("exchanges.dashboard.latency.exchange", "Exchange", ccxt.exchanges)
kraken_latency = rillrate.Pulse("exchanges.dashboard.latency.kraken")
binance_latency = rillrate.Pulse("exchanges.dashboard.latency.binance")

while True:
    start = time.time()
    kraken.fetchTime()
    end = time.time()
    kraken_latency.push(end - start)

    start = time.time()
    binance.fetchTime()
    end = time.time()
    binance_latency.push(end - start)
