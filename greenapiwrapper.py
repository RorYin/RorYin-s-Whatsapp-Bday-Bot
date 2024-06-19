import requests
from setup import *

# api to send Photo by url along with a caption
def SendImgUrl(chatid,fileUrl,text):
    url = f"https://api.greenapi.com/waInstance{InstanceId}/sendFileByUrl/{ApiTokenInstance}"
    # print(chatid,fileUrl,text)
    json_data = {
        'chatId': chatid,
        'urlFile': fileUrl,
        'fileName': 'RorYin.png',
        'caption': text,
    }
    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    print(json_data)
    try:
        resp = requests.post(
            url,
            headers=headers,
            json=json_data,
        )
    except:
        return f"Something went wrong"
    return resp

# api to send message
def SendMsg(chatid,text):
    url = f"https://api.greenapi.com/waInstance{InstanceId}/sendMessage/{ApiTokenInstance}"
    # print(chatid)
    json_data = {
        'chatId': chatid,
        'message': text,
    }
    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    try:
        resp = requests.post(
        url,
        headers=headers,
        json=json_data,
        )
    except:
        return "Something went wrong"
    return resp