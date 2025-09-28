import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = '7754945937:AAEF8uRD6-gvoljh28dAElsV6UNyo2uuuxQ'
OPENAI_KEY = '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'

def ask_gpt(message):
    r = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {OPENAI_KEY}'},
        json={
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': message}]
        }
    )
    return r.json()['choices'][0]['message']['content']

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    reply = ask_gpt(text)
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                  json={'chat_id': chat_id, 'text': reply})
    return 'ok'
