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

print("Bot is running...")
while True:
    schedule.run_pending()
    time.sleep(30)
post_message("✅ البوت يعمل بنجاح! سيتم نشر تحديثات السوق تلقائيًا هنا.")

