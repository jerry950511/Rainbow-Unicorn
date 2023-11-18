from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
from func import *

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    dinner = get_one_restaurant()
    all_restaurant, quantity = get_all_restaurant()
    if message == "晚餐吃什麼":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="不如我們去吃"+dinner+"吧！"))
    elif message == "現在餐廳":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="現在有"+str(quantity)+"間餐廳 分別為:"+",".join(all_restaurant)))   
    elif message.startswith("新增餐廳:"):
        with open('restaurants.json', 'r', encoding='utf8') as f:
            restaurant = json.load(f)
        restaurant.append(message[5:])
        with open('restaurants.json', 'w', encoding='utf8') as f:
            json.dump(restaurant, f, ensure_ascii=False)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已新增餐廳"+message[5:]))
    elif message.startswith("新增餐廳："):
        with open('restaurants.json', 'r', encoding='utf8') as f:
            restaurant = json.load(f)
        restaurant.append(message[5:])
        with open('restaurants.json', 'w', encoding='utf8') as f:
            json.dump(restaurant, f, ensure_ascii=False)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已新增餐廳"+message[5:]))
    elif message.startswith("刪除餐廳:"):
        with open('restaurants.json', 'r', encoding='utf8') as f:
            restaurant = json.load(f)
        try:
            restaurant.remove(message[5:])
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="餐廳不存在"))
            return
        with open('restaurants.json', 'w', encoding='utf8') as f:
            json.dump(restaurant, f, ensure_ascii=False)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="已刪除餐廳"+message[5:]))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)