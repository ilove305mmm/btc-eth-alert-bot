from indicators import (
    get_kline, get_volume_list, get_price_list,
    detect_volume_anomaly, get_open_interest, detect_oi_surge,
    get_liquidation, detect_liquidation_spike,
    detect_delta_volume_breakout, detect_price_volume_oi_sync, detect_depth_absorption_mock
)

def analyze_symbol(symbol):
    kline = get_kline(symbol)
    volumes = get_volume_list(kline)
    prices = get_price_list(kline)
    oi_list = get_open_interest(symbol)
    liq = get_liquidation(symbol)

    # 優先順序：真實突破 > 爆倉 > OI > 成交量 > Delta Volume > 掃單
    if detect_price_volume_oi_sync(kline, oi_list):
        return [f"🚀 {symbol}: 價格 + OI + 成交量齊升，疑似真實突破！"]
    if detect_liquidation_spike(symbol, liq):
        return [f"💥 {symbol}: 爆倉量激增，可能洗盤或踩踏！"]
    if detect_oi_surge(oi_list):
        return [f"📊 {symbol}: OI 激增，可能佈局新倉！"]
    if detect_volume_anomaly(volumes):
        return [f"📈 {symbol}: 異常成交量突破綠K平均！"]
    if detect_delta_volume_breakout(kline):
        return [f"🔄 {symbol}: 主動買單強勢累積，主力吸籌可能啟動！"]
    if detect_depth_absorption_mock(kline):
        return [f"🧱 {symbol}: 掃單打穿上方掛單牆，疑似主力突破！"]

    return []