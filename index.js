
const fetch = require('node-fetch');

const API_KEY = "oirwhz4LaZrywBWgPy";
const API_SECRET = "KtAfP2XkAVh4es5yRZ2CMFB16hXG5Ya01DX";
const crypto = require('crypto');

const getTimestamp = () => Date.now().toString();

function signRequest(params, secret) {
    const orderedParams = Object.keys(params).sort().map(k => k + '=' + params[k]).join('&');
    return crypto.createHmac('sha256', secret).update(orderedParams).digest('hex');
}

async function getOpenInterest(symbol = "BTCUSDT") {
    const url = "https://api.bybit.com/v5/market/open-interest";
    const params = {
        category: "linear",
        symbol,
        intervalTime: 5,
    };

    const timestamp = getTimestamp();
    const queryString = new URLSearchParams(params).toString();
    const signature = signRequest({ ...params, timestamp }, API_SECRET);
    const headers = {
        "X-BAPI-API-KEY": API_KEY,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-SIGN": signature
    };

    try {
        const res = await fetch(`${url}?${queryString}`, { headers });
        const json = await res.json();
        console.log("📈 Open Interest:", json?.result?.list?.[0]);
    } catch (err) {
        console.error("❌ Failed to fetch Open Interest", err);
    }
}

// Main loop
setInterval(() => {
    console.log("🌀 Fetching market data...");
    getOpenInterest();
}, 5000);
