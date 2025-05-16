from indicators import get_kline, get_volume_list, get_cvd_list, detect_volume_spike, detect_cvd_reversal, detect_real_breakout

def analyze_symbol(symbol):
    kline = get_kline(symbol)
    volumes = get_volume_list(kline)
    cvds = get_cvd_list(kline)

    messages = []
    if detect_volume_spike(volumes):
        messages.append(f"📈 {symbol}: 異常成交量突破 20 根綠K！可能為主力行動前兆。")
    if detect_cvd_reversal(cvds):
        messages.append(f"🔄 {symbol}: CVD 出現方向翻轉，可能出現多空轉換！")
    if detect_real_breakout(volumes, cvds):
        messages.append(f"🚀 {symbol}: 符合突破條件，疑似真實突破訊號！")

    return messages