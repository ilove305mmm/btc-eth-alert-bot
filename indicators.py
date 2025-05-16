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
    return [float(candle[5]) for candle in kline]

def get_cvd_list(kline):
    return [float(candle[1]) - float(candle[4]) for candle in kline]  # open - close

def detect_volume_spike(volume_list):
    if len(volume_list) < 2:
        return False
    current = volume_list[-1]
    past_greens = [v for i, v in enumerate(volume_list[:-1]) if i == 0 or volume_list[i] > volume_list[i-1]]
    return current > max(past_greens) if past_greens else False

def detect_cvd_reversal(cvd_list):
    if len(cvd_list) < 2:
        return False
    return cvd_list[-1] * cvd_list[-2] < 0  # sign flip

def detect_real_breakout(volume_list, cvd_list):
    return volume_list[-1] > sum(volume_list[:-1]) / len(volume_list[:-1]) and cvd_list[-1] > 0