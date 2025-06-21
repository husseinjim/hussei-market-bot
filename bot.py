import requests
import time
import schedule
from telegram import Bot

TOKEN = "7506377236:AAFB-Na1T0P80FRM7pZlPo35SqoK75jh6uA"
CHANNEL = "@HusseiAlaswaq"  # Replace with your actual channel username
bot = Bot(token=TOKEN)

def post_message(msg):
    try:
        bot.send_message(chat_id=CHANNEL, text=msg, parse_mode="HTML")
    except Exception as e:
        print(f"Failed to send message: {e}")

def market_snapshot():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "bitcoin,ethereum", "vs_currencies": "usd"}
        prices = requests.get(url, params=params).json()

        gold_price = "2345"
        oil_price = "84.7"

        fng = requests.get("https://api.alternative.me/fng/?limit=1").json()
        fng_value = fng["data"][0]["value"]
        fng_text = fng["data"][0]["value_classification"]

        msg = f"""📊 <b>ملخص الأسواق الآن:</b>
- 🟠 BTC: ${prices['bitcoin']['usd']}
- 🔵 ETH: ${prices['ethereum']['usd']}
- 🟡 الذهب: ${gold_price}
- 🛢️ النفط: ${oil_price}
- 💡 مؤشر الخوف والطمع: {fng_value} ({fng_text})
"""
        post_message(msg)
    except Exception as e:
        print(f"Error in market_snapshot: {e}")

schedule.every().day.at("11:00").do(market_snapshot)
schedule.every().day.at("20:00").do(market_snapshot)
schedule.every().day.at("12:00").do(whale_alert)
schedule.every().day.at("13:00").do(token_listing)
schedule.every().day.at("16:00").do(arabic_news_summary)

print("Bot is running...")
while True:
    schedule.run_pending()
    time.sleep(30)
post_message("✅ البوت يعمل بنجاح! سيتم نشر تحديثات السوق تلقائيًا هنا.")
from datetime import datetime

# === Whale Alert (Mock) ===
def whale_alert():
    fake_data = [
        {"amount": 3100, "symbol": "BTC", "from": "Unknown", "to": "Binance", "value_usd": 94200000}
    ]
    for tx in fake_data:
        msg = f"""🐋 <b>تحرك حوت كبير</b>
تم تحويل {tx['amount']} {tx['symbol']} (~${int(tx['value_usd']/1e6)}M) من {tx['from']} إلى {tx['to']}
⏱️ {datetime.now().strftime('%I:%M %p')} بتوقيت العراق"""
        post_message(msg)

# === Token Listings (Simulated) ===
def token_listing():
    new_token = {
        "name": "ZETA",
        "time": "2:00 ظهراً",
        "url": "https://binance.com/trade/ZETA_USDT"
    }
    msg = f"""🚀 <b>إدراج جديد:</b>
عملة ${new_token['name']} تم إدراجها في منصة Binance  
📆 اليوم الساعة {new_token['time']}  
📈 رابط التداول: {new_token['url']}"""
    post_message(msg)

# === Arabic Crypto News Summary (Placeholder) ===
def arabic_news_summary():
    news_items = [
        "باول: الفيدرالي سيبقي الفائدة حتى نهاية 2025",
        "بيتكوين يقفز فوق 65 ألف بعد دعم مؤسسي",
        "انهيار مشروع NFT وخسائر بملايين"
    ]
    msg = "📰 <b>أبرز الأخبار:</b>\n"
    for i, item in enumerate(news_items, 1):
        msg += f"{i}. {item}\n"
    msg += "\n🧠 هذه الأخبار قد تؤثر على السوق!"
    post_message(msg)

