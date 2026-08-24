import os

import requests

from config import get_settings

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/111.0.0.0 Safari/537.36"
    )
}


def _instance_url(method):
    settings = get_settings()
    instance_id = settings["greenapi_instance_id"]
    token = settings["greenapi_api_token"]
    return f"https://api.greenapi.com/waInstance{instance_id}/{method}/{token}"


def send_image_by_url(chatid, file_url, text):
    json_data = {
        "chatId": chatid,
        "urlFile": file_url,
        "fileName": "RorYin.png",
        "caption": text,
    }
    try:
        response = requests.post(
            _instance_url("sendFileByUrl"),
            headers={**HEADERS, "Content-Type": "application/json"},
            json=json_data,
            timeout=60,
        )
    except Exception as exc:
        return f"Something went wrong: {exc}"
    return response


def send_image_upload(chatid, filepath, text):
    data = {"chatId": chatid, "caption": text}
    try:
        with open(filepath, "rb") as file:
            files = [("file", (os.path.basename(filepath), file, "image/png"))]
            response = requests.post(
                _instance_url("sendFileByUpload"),
                headers=HEADERS,
                data=data,
                files=files,
                timeout=90,
            )
        if response.status_code == 200:
            return f"Success: {response.json()}"
        return f"Failed with status code {response.status_code}: {response.text}"
    except FileNotFoundError:
        return "Error: File not found. Please check the filepath."
    except Exception as exc:
        return f"Something went wrong: {exc}"


def send_message(chatid, text):
    json_data = {"chatId": chatid, "message": text}
    try:
        response = requests.post(
            _instance_url("sendMessage"),
            headers={**HEADERS, "Content-Type": "application/json"},
            json=json_data,
            timeout=60,
        )
    except Exception as exc:
        return f"Something went wrong: {exc}"
    return response


def test_whatsapp_connection(card_path):
    settings = get_settings()
    chatid = settings.get("test_chatid") or settings["default_chatid"]
    return send_image_upload(
        chatid,
        card_path,
        "Test message from RorYin Birthday Bot",
    )


SendImgUrl = send_image_by_url
SendImgUpload = send_image_upload
SendMsg = send_message
