"""Compatibility shim for older imports."""

from config import DATA_FILE, get_settings

_settings = get_settings()
key = _settings["secret_key"]
TgBotToken = _settings["telegram_bot_token"]
devTGid = _settings["telegram_log_chat_id"]
webapppassword = _settings["admin_password"]
display_image_url = _settings["display_image_url"]
default_chatid = _settings["default_chatid"]
InstanceId = _settings["greenapi_instance_id"]
ApiTokenInstance = _settings["greenapi_api_token"]
