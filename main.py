import os
import time
import requests
from telegram import Bot

coins = [
    {"symbol": "PHAUSDT", "tp": 5.88, "sl": 3.30, "name": "PHA", "multiplier": 1}
]

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_USER_ID = "@tolga5"
bot = Bot(token=TELEGRAM_TOKEN)

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

sent_alerts = set()

def get_price_usdt(symbol):
    try:
        res = requests.get(BINANCE_API_URL.format(symbol=symbol), timeout=5)
        res.raise_for_status()
        return float(res.json()['price'])
    except:
        return None

def kontrol_et():
    for coin in coins:
        fiyat = get_price_usdt(coin['symbol'])
        if fiyat is None:
            continue
        fiyat_try = fiyat * coin['multiplier']
        ad = coin['name']
        if fiyat_try >= coin['tp'] and (ad, 'TP') not in sent_alerts:
            bot.send_message(chat_id=TELEGRAM_USER_ID,
                             text=f"🚀 {ad} hedefe ulaştı! ({fiyat_try:.2f} TL)")
            sent_alerts.add((ad, 'TP'))
        elif fiyat_try <= coin['sl'] and (ad, 'SL') not in sent_alerts:
            bot.send_message(chat_id=TELEGRAM_USER_ID,
                             text=f"⚠️ {ad} SL tetiklendi! ({fiyat_try:.2f} TL)")
            sent_alerts.add((ad, 'SL'))

if __name__ == "__main__":
    while True:
        kontrol_et()
        time.sleep(60)

