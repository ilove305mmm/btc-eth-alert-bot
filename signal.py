from indicators import (
    get_kline, get_volume_list, get_cvd_list, get_open_interest,
    get_price_volume, get_liquidation,
    detect_volume_spike, detect_cvd_reversal, detect_real_breakout,
    detect_liquidation_spike, detect_vwap_deviation, detect_oi_surge
)

liq_history = {}

def analyze_symbol(symbol):
    kline = get_kline(symbol)
    volumes = get_volume_list(kline)
    cvds = get_cvd_list(kline)
    pv = get_price_volume(kline)
    oi_list = get_open_interest(symbol)
    liq = get_liquidation(symbol)

    # Maintain liquidation history
    if symbol not in liq_history:
        liq_history[symbol] = []
    liq_history[symbol].append(liq)
    if len(liq_history[symbol]) > 10:
        liq_history[symbol].pop(0)

    messages = []
    if detect_volume_spike(volumes):
        messages.append(f"📈 {symbol}: 異常成交量突破 20 根綠K！")
    if detect_cvd_reversal(cvds):
        messages.append(f"🔄 {symbol}: CVD 出現方向翻轉，可能轉折！")
    if detect_real_breakout(volumes, cvds):
        messages.append(f"🚀 {symbol}: 滿足真實突破條件，疑似主力推動！")
    if detect_liquidation_spike(liq, liq_history[symbol]):
        messages.append(f"💥 {symbol}: 爆倉激增，可能是清洗或逼倉操作！")
    if detect_vwap_deviation(pv):
        messages.append(f"⚠️ {symbol}: 價格大幅偏離 VWAP，注意回歸風險！")
    if detect_oi_surge(oi_list):
        messages.append(f"📊 {symbol}: OI 激增，可能有新大單或佈局！")
    return messages