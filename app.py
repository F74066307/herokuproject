import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "state1", "state2","state3","state4","state5","state6"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state1",
            "conditions": "hello",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state2",
            "conditions": "bye",
        },
        {"trigger": "go_back", "source": ["state1", "state2"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

textlist[
    "在想些什麼嗎?"
    "聽些歌吧\nhttps://www.youtube.com/playlist?list=PL1NeGg1woXqlISJkxjgwHKgB8LmR7tk92"
    "看些影片嗎?\nhttps://www.youtube.com/playlist?list=PL1NeGg1woXqk0_YA5OJkJZoibyqyqsUE9"
    "是否是累了呢"
    "一時找不到的東西往往都在身邊，轉過頭去看看吧"
    "覺得這世界無趣?正巧，我也是"
    "正如同我無法給予你什麼一樣，你也無法給任何人什麼"
    "悲傷吧，哀慟吧，那便是你活著的證明"
    "那是一個美好的日子，花兒綻放著，鳥兒在鳴叫，在這樣的日子裡，一個像你一樣的孩子…\n就該在地獄里焚燒殆盡\nhttps://youtu.be/wDgQdr8ZkTw"
]

hologura="https://www.youtube.com/playlist?list=PL1NeGg1woXqmEelvJb_OFtVi8iYJgNF6D"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

            if event.message.text.find("聽歌")!=-1:
                text="https://www.youtube.com/playlist?list=PL1NeGg1woXqlISJkxjgwHKgB8LmR7tk92"
            elif event.message.text.find("ホロぐら")!=-1 or event.message.text.find("hologura")!=-1:
                text=hologura
            elif event.message.text.find("剪輯")!=-1 or event.message.text.find("切り抜き")!=-1:
                text="https://www.youtube.com/playlist?list=PL1NeGg1woXqk0_YA5OJkJZoibyqyqsUE9"
            elif event.message.text.find("ASMR")!=-1:
                text="https://www.youtube.com/playlist?list=PL1NeGg1woXqlNFSy_AW3x6RwTqP5rTM_c"
            elif event.message.text.find("mio")!=-1 or event.message.text.find("ookami")!=-1 or event.message.text.find("大神")!=-1 or event.message.text.find("ミオ")!=-1:
                text="https://www.youtube.com/channel/UCp-5t9SrOQwXMU7iIjQfARg"
            else :
                text=random.choice(textlist)
　　　　　　
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
