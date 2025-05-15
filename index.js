
const fetch = require('node-fetch');
const crypto = require('crypto');

const API_KEY = "oirwhz4LaZrywBWgPy";
const API_SECRET = "KtAfP2XkAVh4es5yRZ2CMFB16hXG5Ya01DX";

function getTimestamp() {
    return Date.now().toString();
}

function signRequest(params, secret) {
    const orderedParams = Object.keys(params).sort().map(k => k + '=' + params[k]).join('&');
    return crypto.createHmac('sha256', secret).update(orderedParams).digest('hex');
}

async function getOpenInterest(symbol = "BTCUSDT") {
    const baseUrl = "https://api.bybit.com/v5/market/open-interest";
    const params = {
        category: "linear",
        symbol: symbol,
        intervalTime: "5"
    };
    const timestamp = getTimestamp();
    const query = new URLSearchParams(params).toString();
    const signature = signRequest({ ...params, timestamp }, API_SECRET);

    const headers = {
        "X-BAPI-API-KEY": API_KEY,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-SIGN": signature
    };

    try {
        const response = await fetch(`${baseUrl}?${query}`, { method: "GET", headers });
        const text = await response.text();
        try {
            const json = JSON.parse(text);
            console.log("✅ Open Interest:", json?.result?.list?.[0]);
        } catch (e) {
            console.error("⚠️ Unexpected response (not JSON):", text);
        }
    } catch (err) {
        console.error("❌ Fetch error:", err.message);
    }
}

setInterval(() => {
    console.log("🔄 Fetching market data...");
    getOpenInterest();
}, 5000);
