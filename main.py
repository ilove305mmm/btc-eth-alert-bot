import requests
import time
from datetime import datetime

# Telegram config
TELEGRAM_TOKEN = "7832725484:AAFetGmUw2UWZmcgX46Im3llWuDHaARjPGA"
TELEGRAM_CHAT_ID = "7574994738"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=data)
        print("Sent:", message)
    except Exception as e:
        print("Telegram Error:", str(e))

def get_volume(symbol="BTCUSDT"):
    try:
        response = requests.get(
            "https://api.bybit.com/v5/market/kline",
            params={
                "category": "linear",
                "symbol": symbol,
                "interval": "5",
                "limit": 20
            }
        )
        data = response.json()
        volume_list = [float(i[5]) for i in data["result"]["list"]]
        return volume_list
    except Exception as e:
        print("Volume Error:", str(e))
        return []

def detect_volume_spike(volumes):
    if not volumes or len(volumes) < 2:
        return False
    current = volumes[-1]
    past_greens = [v for i, v in enumerate(volumes[:-1]) if i == 0 or volumes[i] > volumes[i-1]]
    return current > max(past_greens) if past_greens else False

def main():
    # Send a forced test message at startup
    send_telegram("🚨 測試訊息：Render 上的程式已啟動並正常運作！")

    while True:
        print(f"[{datetime.now()}] Running scan...")
        for symbol in ["BTCUSDT", "ETHUSDT"]:
            volumes = get_volume(symbol)
            if detect_volume_spike(volumes):
                send_telegram(f"📈 {symbol}: 異常成交量突破 20 根綠K！")
        time.sleep(300)

if __name__ == "__main__":
    main()