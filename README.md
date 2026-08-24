![](https://telegra.ph/file/b1f62ac15f2b9eca174ba.png)

 ![Adobe Photoshop](https://img.shields.io/badge/adobe%20photoshop-%2331A8FF.svg?style=for-the-badge&logo=adobe%20photoshop&logoColor=white)![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)

![](https://img.shields.io/github/stars/RorYin/RorYin-s-Whatsapp-Bday-Bot.svg) ![](https://img.shields.io/github/forks/RorYin/RorYin-s-Whatsapp-Bday-Bot.svg) ![](https://img.shields.io/github/tags/RorYin/RorYin-s-Whatsapp-Bday-Bot.svg) ![](https://img.shields.io/github/release/RorYin/RorYin-s-Whatsapp-Bday-Bot.svg) ![](https://img.shields.io/github/issues/RorYin/RorYin-s-Whatsapp-Bday-Bot.svg)

# RorYin's WhatsApp Birthday Bot

Flask dashboard that stores birthdays in `data.json`, sends WhatsApp group wishes through [Green API](https://green-api.com/), and logs results to a Telegram group.

## Features

+ Can post birthday and work-anniversary wishes on a WhatsApp group.
+ Names are written onto random card templates.
+ Web UI to edit people data (admin) and API/setup keys (superadmin).
+ Completely free of cost; hosting might cost a small sum.
+ WhatsApp API from Green API (a practical alternative to many paid APIs).
+ Free Green API allows 3 chats and 1000 messages per month, usually enough for a group of 200+.
+ Currently intended to run on PythonAnywhere with a daily scheduled task.

## Easy setup (local)

1. Clone the repo and install Python 3.10+ (3.11 is a good match for PythonAnywhere).
2. Install packages:

```bash
pip install -r requirements.txt
```

3. Copy settings and fill in your keys:

```bash
copy settings.example.json settings.json
```

On Linux / PythonAnywhere:

```bash
cp settings.example.json settings.json
```

Edit `settings.json`:

| Field | What to put |
|---|---|
| `admin_password` | Password for the Data and Actions tabs |
| `superadmin_password` | Password that also unlocks Setup (API keys) |
| `secret_key` | Any long random string for Flask sessions |
| `telegram_bot_token` | Token from [@BotFather](https://t.me/BotFather) |
| `telegram_log_chat_id` | Telegram group/chat id for logs (add the bot to the group) |
| `greenapi_instance_id` | Instance id from [green-api.com](https://green-api.com/) |
| `greenapi_api_token` | Instance API token from Green API |
| `default_chatid` | WhatsApp group chat id (`...@g.us`) |
| `test_chatid` | Chat used by **Test WhatsApp API** |
| `timezone` | `Asia/Calcutta` unless you need another zone |
| `work_anniversary_image` | Filename only; file must live in `templates/` |

4. Keep `data.json` next to `app.py` (or start with `[]`).
5. Run:

```bash
python app.py
```

Open the printed local URL, sign in, and use **Data** / **Actions** / **Setup**.

Dates in the UI are `dd/mm/yyyy`. Empty optional fields save as `NA`.

## Deploy on PythonAnywhere

This is the recommended host because you can schedule `Task.py` once a day.

### 1. Create the web app

1. Log in at [pythonanywhere.com](https://www.pythonanywhere.com/).
2. **Web** → **Add a new web app** → **Manual configuration** → Python 3.10 or 3.11.
3. Note your site path. For a beginner account this is usually:

```text
/home/<your-username>/mysite
```

### 2. Upload the project

In **Files**, upload the repo into `mysite` so these sit together:

```text
mysite/
  app.py
  Task.py
  config.py
  people.py
  handler.py
  gencard.py
  greenapiwrapper.py
  TGbotHandler.py
  setup.py
  data.json
  settings.json          ← create this on the server, do not commit secrets
  requirements.txt
  templates/             ← HTML + card PNGs + anniversary .webp
  static/
  fonts/
```

Easiest path: `git clone https://github.com/RorYin/RorYin-s-Whatsapp-Bday-Bot.git mysite` in a **Bash** console, then copy `settings.example.json` to `settings.json` and edit it.

### 3. Virtualenv and packages

In a Bash console:

```bash
cd ~
python3 -m venv venv
source venv/bin/activate
pip install -r ~/mysite/requirements.txt
```

On the **Web** tab, set the virtualenv path to `/home/<your-username>/venv`.

### 4. WSGI file

Open the WSGI file from the **Web** tab and replace the contents with:

```python
import sys

project_home = "/home/<your-username>/mysite"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
```

Reload the web app. Visit `https://<your-username>.pythonanywhere.com` and log in.

### 5. Daily WhatsApp task

1. **Tasks** (or **Scheduled tasks**).
2. Add a daily task at the time you want wishes sent (account timezone is usually UTC — convert IST if needed).
3. Command:

```bash
/home/<your-username>/venv/bin/python /home/<your-username>/mysite/Task.py
```

`Task.py` checks birthdays and work anniversaries for **today**, sends WhatsApp cards, and logs to Telegram.

On a free account you get a limited number of scheduled tasks. A paid account lets you add more.

### 6. Smoke test from the UI

1. Log in as **admin** or **superadmin**.
2. **Actions** → **Test WhatsApp API** (confirm the popup). A sample card goes to `test_chatid`.
3. **Trigger task** only if you want today's real wishes sent immediately.

## Project files

| File | Role |
|---|---|
| `app.py` | Flask dashboard and APIs |
| `data.json` | People records |
| `settings.json` | Passwords and API keys (local / server only) |
| `handler.py` | Daily birthday + anniversary send |
| `gencard.py` | Birthday card images |
| `greenapiwrapper.py` | Green API WhatsApp calls |
| `TGbotHandler.py` | Telegram logging |
| `Task.py` | Scheduled entry point |

## Tips

+ Confirm Green API is authorized (QR / phone) before expecting sends to work.
+ Card templates are `templates/template1.png` … `template7.png`. Anniversary art is `templates/happy-work-anniversary-6-600x600.webp`.
+ Superadmin **Setup** can change keys in the browser; save asks for confirmation.

Any queries regarding deployment, contact @roryin on TG.

_Star the repo incase if you liked it...! 😊_
