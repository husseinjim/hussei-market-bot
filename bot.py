import requests, time, schedule, xml.etree.ElementTree as ET
from telegram import Bot
from datetime import datetime

TOKEN = "7506377236:AAFB-Na1T0P80FRM7pZlPo35SqoK75jh6uA"
CHANNEL = "@HusseiAlaswaq"
bot = Bot(token=TOKEN)

def post_message(msg):
    try: bot.send_message(chat_id=CHANNEL, text=msg, parse_mode="HTML")
    except Exception as e: print("Post failed:", e)

# 1. Whale Alerts – Daily
def whale_alert_daily():
    txs = requests.get("https://blockchain.info/unconfirmed-transactions?format=json").json().get("txs", [])[:10]
    btc_price = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()['bitcoin']['usd']
    for tx in txs:
        value_btc = sum(o["value"] for o in tx["out"]) / 1e8
        usd = value_btc * btc_price
        if usd >= 5_000_000:
            post_message(f"🐋 <b>تحرك حوت بيتكوين كبير</b>\nتم تحويل {value_btc:.2f} BTC (~${usd/1e6:.1f}M)\n⏱️ {datetime.now():%I:%M %p} بتوقيت العراق")

# 2. Low-Cap Tokens – Hourly
def token_listing():
    coins = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={"vs_currency":"usd","order":"market_cap_asc","per_page":5,"page":1}).json()
    msg = "🚀 <b>إدراجات منخفضة القيمة (CoinGecko):</b>\n"
    for c in coins:
        msg += f"- {c['name']} (${c['symbol'].upper()}) • MC {c['market_cap']:,}\n🔗 https://www.coingecko.com/en/coins/{c['id']}\n"
    post_message(msg + f"\n⏱️ {datetime.now():%I:%M %p} بتوقيت العراق")

# 3. Fear & Greed – Hourly
def fear_greed():
    fng = requests.get("https://api.alternative.me/fng/?limit=1").json()["data"][0]
    post_message(f"💡 <b>مؤشر الخوف والطمع:</b> {fng['value']} ({fng['value_classification']})")

# 4. Market Snapshot – Daily
def market_snapshot():
    pr = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids":"bitcoin,ethereum","vs_currencies":"usd"}).json()
    gold, oil, dxy = 2345, 84.7, 104.2
    fng = requests.get("https://api.alternative.me/fng/?limit=1").json()["data"][0]
    post_message(f"📊 <b>ملخص الأسواق:</b>\n- BTC: ${pr['bitcoin']['usd']}\n- ETH: ${pr['ethereum']['usd']}\n- الذهب: ${gold}\n- النفط: ${oil}\n- DXY: {dxy}\n- الخوف/الطمع: {fng['value']} ({fng['value_classification']})")

# 5. Crypto News – Twice Daily
def arabic_news_summary():
    items = ET.fromstring(requests.get("https://www.coindesk.com/arc/outboundfeeds/rss/").content).findall('.//item')[:3]
    msg = "📰 <b>أحدث الأخبار:</b>\n" + "\n".join(f"{i+1}. {it.find('title').text}" for i, it in enumerate(items))
    post_message(msg + "\n\n🧠 هذه الأخبار قد تؤثر على السوق!")

# 6. Funding Rate Weekly – CoinGlass
def funding_rate_weekly():
    resp = requests.get("https://open-api.coinglass.com/public/v2/funding").json()
    btc = resp.get('data', {}).get('BTC', {}).get('rate', 'N/A')
    eth = resp.get('data', {}).get('ETH', {}).get('rate', 'N/A')
    post_message(f"📈 <b>معدل التمويل الأسبوعي:</b>\n- BTC: {btc}%\n- ETH: {eth}%")

# 7. On-Chain Activity – Every 3 Days
ETHERSCAN_KEY = "2DQWAYKMQ2QRVA156GXZ7MB8QH2TYFTH1Q"
def onchain_activity():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://api.etherscan.io/api?module=stats&action=dailynewaddress&startdate={today}&enddate={today}&apikey={ETHERSCAN_KEY}"
    data = requests.get(url).json().get("result", [])
    if data: post_message(f"🔗 <b>عناوين جديدة ETH اليوم:</b> {data[-1]['newAddressCount']}")

# 8. DeFi TVL – Every 2 Days
def defillama_tvl():
    top5 = sorted(requests.get("https://api.llama.fi/protocols").json(), key=lambda x: x["tvl"], reverse=True)[:5]
    post_message("🏦 <b>أعلى 5 منصات DeFi:</b>\n" + "\n".join(f"- {p['name']}: ${int(p['tvl']):,}" for p in top5))

# 9. Stablecoins Supply – Every 4 Days
def stablecoin_supply():
    msg = "💵 <b>عرض العملات المستقرة:</b>\n"
    for c in ["tether","usd-coin","dai"]:
        supply = int(requests.get(f"https://api.coingecko.com/api/v3/coins/{c}").json()["market_data"]["circulating_supply"])
        msg += f"- {c.upper()}: {supply:,}\n"
    post_message(msg)

# 10. Gas Fees – Daily
def gas_fees():
    gas = requests.get("https://api.blockcypher.com/v1/eth/main").json()["high_fee_per_kb"]/1e9
    post_message(f"🔥 <b>Gas Fee (ETH – high priority):</b> {gas:.1f} Gwei")

# 11. Dominance – Daily
def dominance():
    dom = requests.get("https://api.coingecko.com/api/v3/global").json()["data"]["market_cap_percentage"]
    post_message(f"📌 <b>BTC Dominance:</b> {dom['btc']:.1f}% | <b>ETH Dominance:</b> {dom['eth']:.1f}%")

# 12. Social Trends – Daily via NodeJS wrapper
def social_trend():
    try:
        from subprocess import check_output
        trends = check_output(["node","getTwitterTrends.js"]).decode().splitlines()
        post_message(f"📱 <b>ترند اليوم:</b> {trends[0] if trends else 'N/A'}")
    except Exception as e: print("Twitter trend error:", e)

# Schedule tasks
schedule.every().day.at("10:00").do(whale_alert_daily)
schedule.every().hour.at(":15").do(token_listing)
schedule.every().hour.at(":45").do(fear_greed)
schedule.every().day.at("11:00").do(market_snapshot)
schedule.every().day.at("15:00").do(arabic_news_summary)
schedule.every().monday.at("09:00").do(funding_rate_weekly)
schedule.every(3).days.at("12:00").do(onchain_activity)
schedule.every(2).days.at("12:30").do(defillama_tvl)
schedule.every(4).days.at("13:00").do(stablecoin_supply)
schedule.every().day.at("14:00").do(gas_fees)
schedule.every().day.at("14:30").do(dominance)
schedule.every().day.at("17:00").do(social_trend)

post_message("✅ البوت جاهز وسجل المؤشرات الحية!")  # Startup message

while True:
    schedule.run_pending()
    time.sleep(30)
