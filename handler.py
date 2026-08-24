from datetime import datetime

import pytz

from config import get_settings, work_anniversary_image_path
from gencard import generate_birthday_card
from greenapiwrapper import send_image_upload
from people import load_people, month_day, parse_date
from TGbotHandler import send_log


def _today(timezone_name):
    return datetime.now(pytz.timezone(timezone_name))


def checkbdays():
    settings = get_settings()
    today = _today(settings["timezone"]).strftime("%m-%d")
    log = []
    found = False

    for entry in load_people():
        entry_day = month_day(entry.get("bday", "NA"))
        if not entry_day or entry_day != today:
            continue

        found = True
        name = entry.get("name", "UNKNOWN")
        facts = entry.get("facts", "")
        chatid = entry.get("chatid")
        if not chatid or chatid == "NA":
            chatid = settings["default_chatid"]
        try:
            card_path = generate_birthday_card(name)
            response = send_image_upload(
                chatid,
                card_path,
                f"Happy Birthday {name} 🎉 \n\nFacts/Hobbies:{facts}",
            )
            if "Success" in str(response):
                message = f"Birthday wish sent for {name}"
            else:
                message = f"Birthday wish failed for {name}: {response}"
        except Exception as exc:
            message = f"Birthday wish failed for {name}: {exc}"

        log.append(message)
        send_log(message)

    if not found:
        send_log("No Birthdays today")
    return log


def check_work_anniversaries():
    settings = get_settings()
    now = _today(settings["timezone"])
    today = now.strftime("%m-%d")
    image_path = work_anniversary_image_path(settings)
    log = []

    for entry in load_people():
        joining_date = entry.get("joining_date")
        if not joining_date or joining_date == "NA":
            continue
        try:
            join_date = parse_date(joining_date)
            if join_date is None:
                continue
            if join_date.strftime("%m-%d") != today:
                continue
            years_completed = now.year - join_date.year
            if years_completed <= 0:
                continue

            name = entry.get("name", "UNKNOWN")
            chatid = entry.get("chatid")
            if not chatid or chatid == "NA":
                chatid = settings["default_chatid"]
            caption = (
                f"🎉 Happy Work Anniversary {name}!\n\n"
                f"👏 {years_completed} year"
                f"{'s' if years_completed > 1 else ''} "
                f"of dedication and excellence.\n"
                f"Thank you for being a valuable part of the team!"
            )
            response = send_image_upload(chatid, image_path, caption)
            if "Success" in str(response):
                message = (
                    f"Work anniversary wish sent for {name} ({years_completed} years)"
                )
            else:
                message = f"Work anniversary wish FAILED for {name}: {response}"
            log.append(message)
            send_log(message)
        except Exception as exc:
            name = entry.get("name", "UNKNOWN")
            message = f"Work anniversary error for {name} → {exc}"
            log.append(message)
            send_log(message)

    return log


def run_daily_tasks():
    birthday_log = checkbdays()
    anniversary_log = check_work_anniversaries()
    combined = birthday_log + anniversary_log
    if not combined:
        return ["No birthdays or work anniversaries today."]
    return combined
