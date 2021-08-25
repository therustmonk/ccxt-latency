import ccxt
import rillrate
import time

kraken = ccxt.kraken()
binance = ccxt.binance()

rillrate.install()
exchanges = rillrate.Selector("exchanges.latency.controls.exchange", label="Exchange", options=ccxt.exchanges)
add_button = rillrate.Click("exchanges.latency.controls.add", label="Add")
kraken_latency = rillrate.Pulse("exchanges.latency.charts.kraken")
binance_latency = rillrate.Pulse("exchanges.latency.charts.binance")

while True:
    start = time.time()
    kraken.fetchTime()
    end = time.time()
    kraken_latency.push(end - start)

    start = time.time()
    binance.fetchTime()
    end = time.time()
    binance_latency.push(end - start)
