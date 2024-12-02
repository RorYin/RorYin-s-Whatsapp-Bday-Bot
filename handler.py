from TGbotHandler import logger
import time
from datetime import datetime
import pytz
from setup import *
import json
from greenapiwrapper import *
from gencard import *

bot=logger(TgBotToken)


def checkbdays():
    currentdate = datetime.now(pytz.timezone('Asia/Calcutta')).strftime("%d-%m")
    with open(DATA_FILE, 'r') as file:

        data = json.load(file)
        log = []
    for entry in data:
        date_splits = entry['bday'].split("-")

        the_entry_bday =f"{date_splits[1]}-{date_splits[2]}"

        checked_flag = 0
        if currentdate == the_entry_bday:


            card_path = generate_birthday_card(entry['name'])

            response = SendImgUpload(entry['chatid'],f"./{card_path}",f"Happy Birthday {entry['name']} 🎉")
            print(response)


            checked_flag = 1
            try:
                if ("Success" in response):
                    print(datetime.now(pytz.timezone('Asia/Calcutta')))
                    log.append(f"Birthday wish sent for {entry['name']}")
                    bot.sendMsgTo(devTGid,f"Birthday wish sent for {entry['name']}","","")
                else:
                    log.append(f"Birthday wish sent was failed to sent for {entry['name']}")
                    bot.sendMsgTo(devTGid,f"Birthday wish sent was failed to sent for {entry['name']}","","")
            except Exception as e:
                log.append(f"Birthday wish sent was failed to sent for {entry['name']} {e} response = {response}")
                bot.sendMsgTo(devTGid,f"Birthday wish sent was failed to sent for {entry['name']} {e} response = {response}","","")

    else:
        if(checked_flag == 0):
            bot.sendMsgTo(devTGid,f"No Birthdays today ","","")

    return log