import telebot;
import requests
import threading
import json
import time

token = "<token>"
print("create bot")
bot = telebot.TeleBot(token);
print("created")
url = "https://cre-api.kufar.by/ads-search/v1/engine/v1/search/rendered-paginated"
#payload = {"cat":"1010", "typ": "let", "rng": "6", "ar": "18", "prc": "r:20000,35000", "cur": "BYR", "rms": }
jparams = '{"cat":"1010","typ":"let","rgn":"6","ar":"18","prc":"r:20000,35000","cur":"BYR","rms":"v.or:1,2","rnt":"1","sort":"lst.d","size":"42"}'
payload = json.loads(jparams)
user_id = '<user_id>'

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message)
    bot.send_message(message.from_user.id, "user_id {}".format(message.from_user.id))


old = []
def run_check():
    global old
    print("check")
    try:
        r = requests.get(url, params=payload)
        result = r.json()
        ids = [ads["ad_id"] for ads in result['ads']]
        if ids != old:
            bot.send_message(user_id, "Refreshed")
        old = ids
    except Exception as e:
        bot.send_message(user_id, e)
    threading.Timer(60.0, run_check).start()

print("run threading")
run_check()
print("pooling")
while True:
    try:
        print("start")
        bot.polling(none_stop=True, interval=5)
    except:
        pass
