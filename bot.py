import requests, time, schedule, xml.etree.ElementTree as ET
from telegram import Bot
from datetime import datetime

TOKEN = "7506377236:AAFB-Na1T0P80FRM7pZlPo35SqoK75jh6uA"
CHANNEL = "@alnajimhussein"
bot = Bot(token=TOKEN)
last_messages = {}

def post_message(msg):
    if last_messages.get("last") == msg:
        print("⛔ Duplicate message skipped.")
        return
    try:
        bot.send_message(chat_id=CHANNEL, text=msg, parse_mode="HTML")
        last_messages["last"] = msg
    except Exception as e:
        print("Post failed:", e)

# 1. Whale Alerts – Daily
def whale_alert_daily():
    txs = requests.get("https://blockchain.info/unconfirmed-transactions?format=json").json().get("txs", [])[:10]
    btc_price = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()['bitcoin']['usd']
    for tx in txs:
        value_btc = sum(o["value"] for o in tx["out"]) / 1e8
        usd = value_btc * btc_price
        if usd >= 5_000_000:
            post_message(f"🐋 <b>تحرك حوت بيتكوين كبير</b>\nتم تحويل {value_btc:.2f} BTC (~${usd/1e6:.1f}M)\n⏱️ {datetime.now():%I:%M %p} بتوقيت العراق")

# 2. Low-Cap Tokens – Daily (reduced)
def token_listing():
    coins = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={"vs_currency":"usd","order":"market_cap_asc","per_page":5,"page":1}).json()
    msg = "🚀 <b>إدراجات منخفضة القيمة (CoinGecko):</b>\n"
    for c in coins:
        msg += f"- {c['name']} (${c['symbol'].upper()}) • MC {c['market_cap']:,}\n🔗 https://www.coingecko.com/en/coins/{c['id']}\n"
    post_message(msg + f"\n⏱️ {datetime.now():%I:%M %p} بتوقيت العراق")

# 3. Fear & Greed – Daily (reduced)
def fear_greed():
    fng = requests.get("https://api.alternative.me/fng/?limit=1").json()["data"][0]
    post_message(f"💡 <b>مؤشر الخوف والطمع:</b> {fng['value']} ({fng['value_classification']})")

# 4. Market Snapshot – Daily
def market_snapshot():
    pr = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids":"bitcoin,ethereum","vs_currencies":"usd"}).json()
    gold,
