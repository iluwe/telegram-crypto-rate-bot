import re
from flask_sslify import SSLify
from flask import Flask, request, jsonify
from app.api_requester import *
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
sslify = SSLify(app)


URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

#https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={HOST}/{BOT_TOKEN}


def send_message(chat_id, text):
    """Sending message to user from Bot"""
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


def parse_text(text):
    """Parsing text from user"""
    pattern = r'/\w+'
    slug = re.search(pattern, text).group()
    return slug[1:]


@app.route(f'/{BOT_TOKEN}', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        try:
            chat_id = r['message']['chat']['id']
            message = r['message']['text']
            pattern = r'/\w+'
            if re.search(pattern, message):
                slug = parse_text(message)
                price = get_price(slug)
                send_message(chat_id, text=f'{price} USD')
            else:
                send_message(chat_id, text='Something went wrong\nTry again')
        except KeyError:
            pass
    return '<h1>Bot welcomes you</h1>'


if __name__ == '__main__':
    app.run()
