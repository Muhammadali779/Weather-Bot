import requests
import time

TG_BOT_TOKEN = '7631317956:AAETz8lb2IZkQAlJ0G1qILj70_3XaVePECY'
TG_BOT_BASE_URL = f'https://api.telegram.org/bot{TG_BOT_TOKEN}'
WEATHER_URL = 'http://api.weatherapi.com/v1'
WEATHER_API_KEY = 'c852ebca46f148469f3172212250707'

def get_updates(offset=None):
    url = f"{TG_BOT_BASE_URL}/getUpdates"
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text):
    url = f"{TG_BOT_BASE_URL}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

def get_current_weather(city):
    url = f"{WEATHER_URL}/current.json"
    payload = {'key': WEATHER_API_KEY, 'q': city}
    response = requests.get(url, params=payload)
    data = response.json()
    return data['current']['feelslike_c']

def main():
    print("Bot ishga tushdi...")
    last_update_id = None

    while True:
        updates = get_updates(offset=last_update_id)
        if "result" in updates and len(updates["result"]) > 0:
            for update in updates["result"]:
                message = update.get("message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "").lower()

                if text == "/start":
                    send_message(chat_id, "Salom! Shahar nomini kiriting (masalan: toshkent, samarqand, jizzax).")
                elif text in ["toshkent", "samarqand", "jizzax"]:
                    try:
                        weather = get_current_weather(text)
                        send_message(chat_id, f"Hozir {text.title()}da harorat {weather}°C")
                    except:
                        send_message(chat_id, "Ob-havoni olishda xatolik yuz berdi.")
                else:
                    send_message(chat_id, "Shahar nomini to`g`ri kiriting yoki /start deb yozing.")


                last_update_id = update["update_id"] + 1

        time.sleep(1)

if __name__ == "__main__":
    main()
