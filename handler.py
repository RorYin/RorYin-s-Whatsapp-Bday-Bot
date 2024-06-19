from TGbotHandler import logger
import time
from datetime import datetime
import pytz
from setup import *
import json
from greenapiwrapper import *

bot=logger(TgBotToken)
currentdate = datetime.now(pytz.timezone('Asia/Calcutta')).strftime("%m-%d")

def checkbdays():
    with open(DATA_FILE, 'r') as file:

        data = json.load(file)
        log = []
    for entry in data:
        date_splits = entry['bday'].split("-")

        the_entry_bday =f"{date_splits[1]}-{date_splits[2]}"
        # print(currentdate)
        # print(the_entry_bday)
        if currentdate == the_entry_bday:
            # print(entry)
            # print(entry['name'])
            # print(entry['image_url'])
            # print(entry['chatid'])

            response = SendImgUrl(entry['chatid'],entry['image_url'],f"Happy Birthday {entry['name']} 🎉")
            print(response)
            response = response.json()


            try:
                if(response['idMessage']!=""):
                    print(datetime.now(pytz.timezone('Asia/Calcutta')))
                    log.append(f"Birthday wish sent for {entry['name']}")
                    bot.sendMsgTo(devTGid,f"Birthday wish sent for {entry['name']}","","")
                else:
                    log.append(f"Birthday wish sent was failed to sent for {entry['name']}")
                    bot.sendMsgTo(devTGid,f"Birthday wish sent was failed to sent for {entry['name']}","","")
            except Exception as e:
                log.append(f"Birthday wish sent was failed to sent for {entry['name']} {e} response = {response}")
                bot.sendMsgTo(devTGid,f"Birthday wish sent was failed to sent for {entry['name']} {e} response = {response}","","")

    return log

# print(checkbdays())