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
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="現在有"+str(quantity)+"間餐廳 分別為:"))
        for i in all_restaurant:
            line_bot_api.push_message(event.source.user_id, TextSendMessage(text=i))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)