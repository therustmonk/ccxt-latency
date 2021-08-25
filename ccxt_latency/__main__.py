import ccxt
import rillrate
from rillrate import prime
import time
import threading

rillrate.install()

board = prime.Board("exchanges.latency.parameters.statuses")

class ThreadFlag:
    alive = True

    def stop(self):
        self.alive = False

def measure_latency(name, flag):
    exchange = getattr(ccxt, name)()
    exchange_latency = prime.Pulse("exchanges.latency.charts." + name, min=0, max=5, higher=True)
    board.set(name, "Checking...")
    while flag.alive:
        try:
            start = time.time()
            exchange.fetchStatus()
            end = time.time()
            diff = end - start
            exchange_latency.push(diff)
            board.set(name, str(diff))
        except Exception as e:
            board.set(name, str(e))
            # TODO: Add alert here
            print("Failed", name, e)
        time.sleep(1)

selected_exchange = None
threads = {}
exchanges = prime.Selector("exchanges.latency.controls.exchange", label="Exchange", options=ccxt.exchanges)
def callback(activity, action):
    if action != None:
        global selected_exchange
        selected_exchange = action.value
        exchanges.apply(action.value)
exchanges.sync_callback(callback)

add_button = prime.Click("exchanges.latency.controls.add", label="Add")
def callback(activity, action):
    if action != None:
        add_button.apply()
        flag = ThreadFlag()
        meter = threading.Thread(target=measure_latency, args=(selected_exchange, flag))
        meter.start()
        threads[selected_exchange] = flag
add_button.sync_callback(callback)

del_button = prime.Click("exchanges.latency.controls.remove", label="Remove")
def callback(activity, action):
    if action != None:
        del_button.apply()
        threads[selected_exchange].stop()
        board.remove(selected_exchange)
del_button.sync_callback(callback)

while True:
    time.sleep(1)
