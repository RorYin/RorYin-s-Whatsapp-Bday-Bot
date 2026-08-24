import json
import os
import threading
from datetime import datetime

from config import DATA_FILE

_lock = threading.Lock()

PERSON_FIELDS = ("name", "bday", "image_url", "chatid", "joining_date", "facts")
DATE_FIELDS = ("bday", "joining_date")
DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y")


def _ensure_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)


def load_people():
    _ensure_data_file()
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        return []
    return data


def save_people(people):
    with _lock:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(people, file, indent=4, ensure_ascii=False)


def parse_date(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper() == "NA":
        return None
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def to_iso_date(value, field_name="date"):
    text = "" if value is None else str(value).strip()
    if not text or text.upper() == "NA":
        return "NA"
    parsed = parse_date(text)
    if parsed is None:
        raise ValueError(f"Invalid {field_name}. Use dd/mm/yyyy.")
    return parsed.strftime("%Y-%m-%d")


def month_day(value):
    parsed = parse_date(value)
    if parsed is None:
        return None
    return parsed.strftime("%m-%d")


def normalize_person(payload, defaults=None):
    defaults = defaults or {}
    person = {}
    for field in PERSON_FIELDS:
        value = payload.get(field, defaults.get(field, ""))
        if value is None:
            value = ""
        person[field] = str(value).strip()
    if not person["name"]:
        raise ValueError("Name is required.")
    for field in PERSON_FIELDS:
        if field != "name" and not person[field]:
            person[field] = "NA"
    for field in DATE_FIELDS:
        person[field] = to_iso_date(person[field], "birthday" if field == "bday" else "joining date")
    return person


def add_person(payload, default_chatid=None, display_image_url=None):
    person = normalize_person(payload)
    people = load_people()
    people.append(person)
    save_people(people)
    return person, len(people) - 1


def update_person(index, payload, default_chatid=None, display_image_url=None):
    people = load_people()
    if index < 0 or index >= len(people):
        raise IndexError("Person not found.")
    person = normalize_person(payload)
    people[index] = person
    save_people(people)
    return person


def delete_person(index):
    people = load_people()
    if index < 0 or index >= len(people):
        raise IndexError("Person not found.")
    removed = people.pop(index)
    save_people(people)
    return removed
