from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load environment variables
WHATSAPP_API_URL = os.environ['WHATSAPP_API_URL']
WHATSAPP_ACCESS_TOKEN = os.environ['WHATSAPP_ACCESS_TOKEN']
WHATSAPP_PHONE_NUMBER_ID = os.environ['WHATSAPP_PHONE_NUMBER_ID']
FLOW_ID = os.environ['FLOW_ID']

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                if change.get('field') == 'messages':
                    for message in change.get('value', {}).get('messages', []):
                        if message.get('type') == 'text':
                            from_number = message['from']
                            send_flow_to_user(from_number)
    return jsonify({'status': 'received'}), 200

def send_flow_to_user(phone_number):
    url = f"{WHATSAPP_API_URL}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {
                "type": "text",
                "text": "Welcome to our service!"
            },
            "body": {
                "text": "Please select an option"
            },
            "footer": {
                "text": "Footer text"
            },
            "action": {
                "button": "Options",
                "sections": [
                    {
                        "title": "Section 1",
                        "rows": [
                            {
                                "id": "option1",
                                "title": "Option 1",
                                "description": "Description for option 1"
                            },
                            {
                                "id": "option2",
                                "title": "Option 2",
                                "description": "Description for option 2"
                            }
                        ]
                    }
                ]
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"Message sent to {phone_number}")
    else:
        print(f"Failed to send message to {phone_number}: {response.text}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
