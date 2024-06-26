import requests



headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

class logger():
    def __init__(self,token):

        self.url=f"https://api.telegram.org/bot{token}/"
        self.token=token

# Method to send message using chat id
    def sendMsgTo(self,chat_id,msg,msg_id,markdown):
        params={
            "reply_to_message_id":msg_id,
            "allow_sending_without_reply":True,
            "chat_id":chat_id,
            "text":msg,
            "parse_mode":markdown
            }

        response=requests.get(f"https://api.telegram.org/bot{self.token}/sendMessage",headers=headers,params=params)
        if(response.status_code!=202):
            print(response.status_code)

# Method to message along with text
    def sendPhoto(self,imgurl,text,chat_id,msg_id,markdown):
        #send message
        params={
            "chat_id":chat_id,
            "allow_sending_without_reply":True,
            "reply_to_message_id":msg_id,
            "photo":imgurl,
            "caption":text,
            "parse_mode":markdown
        }
        try:
            response=requests.get(f"https://api.telegram.org/bot{self.token}/sendPhoto",headers=headers,params=params)
            if(response.status_code!=202):
                print(response.status_code)
        except:
            print("In logger module ,problem with requests")

# Method to delete a sent message
    def deleteMessage(self,chat_id,message_id):
        #delete the message
        params={
            "chat_id":chat_id,
            "message_id":message_id
        }
        try:
            response=requests.get(f"https://api.telegram.org/bot{self.token}/deleteMessage",headers=headers,params=params)
            if(response.status_code!=202):
                print(response.status_code)
        except:
            print("In logger module ,problem with requests")