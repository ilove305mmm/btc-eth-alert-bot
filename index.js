const express = require('express');
const fetch = require('node-fetch');
const app = express();
const PORT = process.env.PORT || 3000;

const TELEGRAM_BOT_TOKEN = '7832725484:AAFetGmUw2UWZmcgX46Im3llWuDHaARjPGA';
const TELEGRAM_CHAT_ID = '7574994738';

let lastVolume = { BTC: [], ETH: [] };
let lastCVD = { BTC: null, ETH: null };
let lastCVDTrend = { BTC: null, ETH: null };

async function sendTelegramMessage(msg) {
  const url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
  await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: TELEGRAM_CHAT_ID,
      text: msg
    })
  });
}

function getFakeData(symbol) {
  const randVol = Math.floor(400 + Math.random() * 400);
  const randCVD = Math.floor(Math.random() * 100000);
  return { volume: randVol, cvd: randCVD };
}

function checkVolumeSpike(symbol, currentVol) {
  const history = lastVolume[symbol];
  if (history.length < 20) return false;
  return currentVol > Math.max(...history);
}

function checkCVDTrendChange(symbol, currentCVD) {
  const prev = lastCVD[symbol];
  const prevTrend = lastCVDTrend[symbol];
  if (prev === null) {
    lastCVD[symbol] = currentCVD;
    return null;
  }
  const trend = currentCVD > prev ? 'up' : (currentCVD < prev ? 'down' : prevTrend);
  const changed = trend !== prevTrend && prevTrend !== null;
  lastCVD[symbol] = currentCVD;
  lastCVDTrend[symbol] = trend;
  return changed ? trend : null;
}

app.get('/', async (req, res) => {
  const symbols = ['BTC', 'ETH'];
  for (const sym of symbols) {
    const { volume, cvd } = getFakeData(sym);

    if (checkVolumeSpike(sym, volume)) {
      await sendTelegramMessage(`🔔 [${sym}] Volume Spike!\nCurrent: ${volume}, Past Max: ${Math.max(...lastVolume[sym])}`);
    }

    const cvdTrend = checkCVDTrendChange(sym, cvd);
    if (cvdTrend) {
      await sendTelegramMessage(`🔄 [${sym}] CVD Reversal!\nNew Direction: ${cvdTrend}`);
    }

    lastVolume[sym].push(volume);
    if (lastVolume[sym].length > 20) lastVolume[sym].shift();
  }

  res.send('✅ Monitoring BTC + ETH...');
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
