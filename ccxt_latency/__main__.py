import ccxt
import rillrate
import time
import threading

rillrate.install()

board = rillrate.Board("exchanges.latency.parameters.statuses")

def measure_latency(name):
    alive = True
    exchange = getattr(ccxt, name)()
    exchange_latency = rillrate.Pulse("exchanges.latency.charts." + name, min=0, max=5, higher=True)
    board.set(name, "Checking...")
    while alive:
        try:
            start = time.time()
            exchange.fetchTime()
            end = time.time()
            diff = end - start
            exchange_latency.push(diff)
            board.set(name, str(diff))
            time.sleep(1)
        except Exception as e:
            board.set(name, str(e))
            # TODO: Add alert here
            print("Failed", name, e)
            time.sleep(5)
            continue

selected_exchange = None
exchanges = rillrate.Selector("exchanges.latency.controls.exchange", label="Exchange", options=ccxt.exchanges)
def callback(activity, action):
    print("Selected", activity, action)
    if action != None:
        global selected_exchange
        selected_exchange = action.value
        exchanges.apply(action.value)
exchanges.sync_callback(callback)

add_button = rillrate.Click("exchanges.latency.controls.add", label="Add")
def callback(activity, action):
    if action != None:
        add_button.apply()
        meter = threading.Thread(target=measure_latency, args=(selected_exchange,))
        meter.start()
add_button.sync_callback(callback)

while True:
    time.sleep(1)
