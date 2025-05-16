import requests
import time
from datetime import datetime
from signal import analyze_symbol

TELEGRAM_TOKEN = "7832725484:AAFetGmUw2UWZmcgX46Im3llWuDHaARjPGA"
TELEGRAM_CHAT_ID = "7574994738"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Telegram Error:", str(e))

def main():
    send_telegram("✅ V4 主力監控版已啟動！")
    while True:
        print(f"[{datetime.now()}] Running analysis...")
        for symbol in ["BTCUSDT", "ETHUSDT"]:
            messages = analyze_symbol(symbol)
            for msg in messages:
                send_telegram(msg)
        time.sleep(300)

if __name__ == "__main__":
    main()