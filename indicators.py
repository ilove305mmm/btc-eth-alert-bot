import requests

def get_kline(symbol="BTCUSDT", limit=20):
    url = "https://api.bybit.com/v5/market/kline"
    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": "5",
        "limit": limit
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data["result"]["list"]
    except Exception as e:
        print("Kline error:", str(e))
        return []

def get_volume_list(kline):
    return [float(c[5]) for c in kline]

def get_price_list(kline):
    return [float(c[4]) for c in kline]

def detect_volume_anomaly(volume_list):
    if len(volume_list) < 2:
        return False
    current = volume_list[-1]
    greens = [v for i, v in enumerate(volume_list[:-1]) if volume_list[i] > volume_list[i-1]]
    if not greens:
        return False
    avg = sum(greens) / len(greens)
    return current > avg

def get_open_interest(symbol="BTCUSDT"):
    url = "https://api.bybit.com/v5/market/open-interest"
    params = {
        "category": "linear",
        "symbol": symbol,
        "intervalTime": "5"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return [float(i["openInterest"]) for i in data["result"]["list"]]
    except Exception as e:
        print("OI error:", str(e))
        return []

def detect_oi_surge(oi_list):
    if len(oi_list) < 2:
        return False
    current = oi_list[-1]
    avg = sum(oi_list[:-1]) / len(oi_list[:-1])
    return current > avg * 1.5

liq_history = {}
def get_liquidation(symbol="BTCUSDT"):
    url = "https://api.bybit.com/v5/market/liquidation"
    params = {
        "category": "linear",
        "symbol": symbol,
        "limit": 20
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return sum(float(i["qty"]) for i in data["result"]["list"])
    except Exception as e:
        print("Liquidation error:", str(e))
        return 0

def detect_liquidation_spike(symbol, liq):
    global liq_history
    if symbol not in liq_history:
        liq_history[symbol] = []
    liq_history[symbol].append(liq)
    if len(liq_history[symbol]) > 10:
        liq_history[symbol].pop(0)
    if len(liq_history[symbol]) < 5:
        return False
    avg = sum(liq_history[symbol]) / len(liq_history[symbol])
    return liq > avg * 2.5

def detect_delta_volume_breakout(kline):
    deltas = [float(c[4]) - float(c[1]) for c in kline]  # close - open
    return deltas[-1] > 0 and deltas[-1] > sum(deltas[-5:-1]) / 4

def detect_price_volume_oi_sync(kline, oi_list):
    if len(kline) < 2 or len(oi_list) < 2:
        return False
    return (
        float(kline[-1][4]) > float(kline[-2][4]) and
        float(kline[-1][5]) > float(kline[-2][5]) and
        oi_list[-1] > oi_list[-2]
    )

def detect_depth_absorption_mock(kline):
    last = kline[-1]
    open_price = float(last[1])
    close_price = float(last[4])
    return close_price - open_price > abs(open_price * 0.002)