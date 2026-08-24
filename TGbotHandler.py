import requests

from config import get_settings

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    )
}


def send_log(message):
    settings = get_settings()
    token = settings["telegram_bot_token"]
    chat_id = settings["telegram_log_chat_id"]
    if not token or not chat_id:
        return
    try:
        requests.get(
            f"https://api.telegram.org/bot{token}/sendMessage",
            headers=HEADERS,
            params={
                "chat_id": chat_id,
                "text": message,
                "allow_sending_without_reply": True,
            },
            timeout=30,
        )
    except Exception as exc:
        print(f"Telegram log failed: {exc}")


class logger:
    def __init__(self, token):
        self.token = token

    def sendMsgTo(self, chat_id, msg, msg_id, markdown):
        send_log(msg)

    def sendPhoto(self, imgurl, text, chat_id, msg_id, markdown):
        send_log(text)

    def deleteMessage(self, chat_id, message_id):
        return None
