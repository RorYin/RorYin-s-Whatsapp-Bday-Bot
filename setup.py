from cryptography.fernet import Fernet

key = Fernet.generate_key()

DATA_FILE = 'data.json'

TgBotToken = "Place ur TG Bot Token here"

devTGid = "Your TG account ID"  #will be used for later implementation of error log in Telegram group as telegram apis are very reliable.

webapppassword = "WebpagePassword"
#webapp password

display_image_url = "https://telegra.ph/file/c3f382697478e3e9f1887.png"
# url for the image that will be sent along with the text

default_chatid =   "chatid/groupid of whatsapp" #Get it from greenapi 
# Whatsapp group chatid where bot should send posts

# greenapi instance id
InstanceId = "greenapi instance id" 

#greenapi api token instance
ApiTokenInstance = "greenapi token instance" 



