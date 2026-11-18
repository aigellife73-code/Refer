import os
import time
import random
import requests

TELEGRAM_BOT_TOKEN = "9019675422:AAHczIEp7XDWvMtrmbrVAdrSGRHizWGMo7E"
TELEGRAM_CHAT_ID = "5773956827"
UOTP_API_KEY = "7tipmJREBWqRX9X1cUA9eai6CusF0xlwLYmpKVWD"
REFERRAL_CODE = "ARU29SA"

UOTP_BASE_URL = "https://uotp.store/api/stubs/handler_api.php"
PAYZUVA_URL = "https://okmgi.paykexo.com/api/register"  # Naya domain endpoint

is_running = False
target_count = 0
last_update_id = 0

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        print("Telegram Error:", e)

def get_uotp_number():
    # UOTP API se number fetch karne ka request
    url = f"{UOTP_BASE_URL}?api_key={UOTP_API_KEY}&action=getNumber&service=other"
    try:
        res = requests.get(url, timeout=10).text
        if "ACCESS_NUMBER" in res:
            parts = res.split(":")
            return parts[1], parts[2] # activation_id, phone number
    except Exception as e:
        print("UOTP Error:", e)
    return None, None

def check_telegram_commands():
    global is_running, target_count, last_update_id
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=2"
    try:
        res = requests.get(url, timeout=5).json()
        if res.get("result"):
            for update in res["result"]:
                last_update_id = update["update_id"]
                msg = update.get("message", {}).get("text", "").strip()
                
                if msg.startswith("/start"):
                    parts = msg.split()
                    if len(parts) > 1 and parts[1].isdigit():
                        target_count = int(parts[1])
                    else:
                        target_count = 5
                    is_running = True
                    send_telegram(f"🚀 *Render Bot Started!*\nTarget: `{target_count}` referrals for `okmgi.paykexo.com`.")
                elif msg == "/stop":
                    is_running = False
                    send_telegram("🛑 *Bot Stopped by user!*")
    except Exception as e:
        print("Command Check Error:", e)

if __name__ == "__main__":
    send_telegram("🤖 *Render Background Bot Online hai!*\n\nCommands:\n• `/start 5` (5 referrals ke liye)\n• `/stop` (Rokne ke liye)")
    print("Bot is running on Render...")

    while True:
        check_telegram_commands()
        
        if is_running:
            for i in range(1, target_count + 1):
                check_telegram_commands()
                if not is_running:
                    break
                
                send_telegram(f"🔍 *Attempt {i}/{target_count}:* UOTP se number fetch ho raha hai...")
                
                activation_id, phone = get_uotp_number()
                
                if not phone:
                    send_telegram("⚠️ UOTP se number nahi mila ya balance khatam hai!")
                    is_running = False
                    break
                
                password = f"Pass@{random.randint(1000, 9999)}!#"
                
                payload = {
                    "phone": phone,
                    "password": password,
                    "invite_code": REFERRAL_CODE
                }
                
                try:
                    response = requests.post(PAYZUVA_URL, json=payload, timeout=10)
                    report = (
                        f"📊 *Referral Status ({i}/{target_count})*\n\n"
                        f"📱 *Phone:* `{phone}`\n"
                        f"⚡ *Status:* `{response.status_code}`\n"
                        f"📄 *Response:* \n```{response.text[:200]}```"
                    )
                    send_telegram(report)
                except Exception as e:
                    send_telegram(f"🔥 *Request Error:* `{str(e)}`")
                
                time.sleep(5)
                
            is_running = False
            send_telegram("🏁 *Batch Completed!*")
            
        time.sleep(2)
