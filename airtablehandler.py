from setup import *
import requests
import time
import datetime
from greenapiwrapper import *
import random
import json
from TGbotHandler import logger

bot=logger(TgBotToken)


imgurls = ['https://telegra.ph/file/c3f382697478e3e9f1887.png','https://telegra.ph/file/93502be93dcee34d0191a.png','https://telegra.ph/file/45b370a3d53f2b88b6ad9.png']
def ToCheckIfAnyBdayToday():
    headers = {
        'Authorization': f'Bearer {AirtableToken}',
    }
    Response = requests.get(f"https://api.airtable.com/v0/{BaseId}/{TableId}?fields%5B%5D=Name&fields%5B%5D=bday&fields=chatid",headers=headers).json()
    data = Response['records']
    for i in data:
        dt_today = datetime.datetime.today()
        currentdate = dt_India = dt_today.astimezone().strftime("%d-%m")
        if(currentdate == i['fields']['bday']):
            response = SendImgUrl(i['fields']['chatid'],random.choice(imgurls),f"Happy Birthday {i['fields']['Name']} 🎉")
            response = response.json()
            # print(response['idMessage'])
            try:
                if(response['idMessage']!=""):
                    bot.sendMsgTo(devTGid,f"Birthday wish sent for {i['fields']['Name']}","","")
                else:
                    bot.sendMsgTo(devTGid,f"Birthday wish sent was failed to sent for {i['fields']['Name']}","","")
            except:
                bot.sendMsgTo(devTGid,f"Birthday wish sent was failed to sent for {i['fields']['Name']}","","")

