import time

def get_kline(symbol="BTCUSDT", limit=20):
    import requests
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
    return [float(candle[5]) for candle in kline]

def get_cvd_list(kline):
    return [float(candle[1]) - float(candle[4]) for candle in kline]  # open - close

def get_price_volume(kline):
    return [(float(candle[4]), float(candle[5])) for candle in kline]  # close, volume

def get_open_interest(symbol="BTCUSDT"):
    import requests
    url = "https://api.bybit.com/v5/market/open-interest"
    params = {
        "category": "linear",
        "symbol": symbol,
        "intervalTime": "5"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return [float(item["openInterest"]) for item in data["result"]["list"]]
    except Exception as e:
        print("OI error:", str(e))
        return []

def get_liquidation(symbol="BTCUSDT"):
    import requests
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

def detect_volume_spike(volume_list):
    if len(volume_list) < 2:
        return False
    current = volume_list[-1]
    past_greens = [v for i, v in enumerate(volume_list[:-1]) if i == 0 or volume_list[i] > volume_list[i-1]]
    return current > max(past_greens) if past_greens else False

def detect_cvd_reversal(cvd_list):
    if len(cvd_list) < 2:
        return False
    return cvd_list[-1] * cvd_list[-2] < 0

def detect_real_breakout(volume_list, cvd_list):
    return volume_list[-1] > sum(volume_list[:-1]) / len(volume_list[:-1]) and cvd_list[-1] > 0

def detect_liquidation_spike(liq, liq_history):
    if not liq_history:
        return False
    avg_liq = sum(liq_history) / len(liq_history)
    return liq > avg_liq * 2.5

def detect_vwap_deviation(price_volume):
    import statistics
    if len(price_volume) < 5:
        return False
    prices, volumes = zip(*price_volume)
    vwap = sum(p * v for p, v in price_volume) / sum(volumes)
    std = statistics.stdev(prices)
    last_price = prices[-1]
    return abs(last_price - vwap) > std * 1.5

def detect_oi_surge(oi_list):
    if len(oi_list) < 2:
        return False
    current = oi_list[-1]
    avg = sum(oi_list[:-1]) / len(oi_list[:-1])
    return current > avg * 1.5