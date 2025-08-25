import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("WHATSAPP_TOKEN")
phone_number_id = os.getenv("PHONE_NUMBER_ID")
url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"


class SendMessage:
    def __init__ (self):
        self.token = os.getenv("WHATSAPP_TOKEN")
        self.phone_id = os.getenv("PHONE_NUMBER_ID")

    def send (self, message, to="5598991044381"):
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message}
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()

if __name__ == "__main__":
    client = SendMessage()
    client.send("Mensagem Inicial")