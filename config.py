import json
import os
import threading

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
DATA_FILE = os.path.join(BASE_DIR, "data.json")
TEMP_DIR = os.path.join(BASE_DIR, "temp")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

_lock = threading.Lock()

DEFAULT_SETTINGS = {
    "admin_password": "change-me-admin",
    "superadmin_password": "change-me-superadmin",
    "secret_key": "change-this-flask-secret",
    "telegram_bot_token": "",
    "telegram_log_chat_id": "",
    "greenapi_instance_id": "",
    "greenapi_api_token": "",
    "default_chatid": "",
    "test_chatid": "",
    "display_image_url": "",
    "timezone": "Asia/Calcutta",
    "work_anniversary_image": "happy-work-anniversary-6-600x600.webp",
}

SENSITIVE_SETTING_KEYS = (
    "admin_password",
    "superadmin_password",
    "secret_key",
    "telegram_bot_token",
    "telegram_log_chat_id",
    "greenapi_instance_id",
    "greenapi_api_token",
    "default_chatid",
    "test_chatid",
)


def _ensure_settings_file():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(DEFAULT_SETTINGS, file, indent=4)


def get_settings():
    _ensure_settings_file()
    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        stored = json.load(file)
    merged = dict(DEFAULT_SETTINGS)
    merged.update(stored)
    return merged


def save_settings(updates):
    with _lock:
        current = get_settings()
        for key, value in updates.items():
            if key not in DEFAULT_SETTINGS:
                raise ValueError(f"Unknown setting: {key}")
            current[key] = value if isinstance(value, str) else str(value)
        current["work_anniversary_image"] = os.path.basename(
            current.get("work_anniversary_image") or "happy-work-anniversary-6-600x600.webp"
        )
        with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
            json.dump(current, file, indent=4)
        return current


def work_anniversary_image_path(settings=None):
    settings = settings or get_settings()
    filename = os.path.basename(settings.get("work_anniversary_image") or "")
    if not filename:
        filename = "happy-work-anniversary-6-600x600.webp"
    return os.path.join(TEMPLATES_DIR, filename)


def public_settings(settings, is_superadmin):
    if is_superadmin:
        return {key: settings[key] for key in DEFAULT_SETTINGS}
    return {
        "timezone": settings["timezone"],
        "default_chatid": settings["default_chatid"],
        "display_image_url": settings["display_image_url"],
    }
