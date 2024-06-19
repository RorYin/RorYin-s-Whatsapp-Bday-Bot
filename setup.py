from cryptography.fernet import Fernet

key = Fernet.generate_key()

DATA_FILE = 'data.json'

TgBotToken = "5851812153:AAFqyJ5lgaxIrWJhC6HDCKIGzXN_ojncgVs"

devTGid = "-4062855842"  #will be used for later implementation of error log in Telegram group as telegram apis are very reliable.

webapppassword = "roryin"
#webapp password

display_image_url = "https://telegra.ph/file/c3f382697478e3e9f1887.png"
# url for the image that will be sent along with the text

default_chatid =   "919986016721-1453656300@g.us"  #"919128830436-1624964186@g.us"
# Whatsapp group chatid where bot should send posts

# greenapi instance id
InstanceId = "7103881557" #"7103881919"

#greenapi api token instance
ApiTokenInstance = "e854ca40a03448048d9438650b239487360317b0c0524bf09e" #"fc540920e4444202beb809deea4e0c32489714616ed646cda5"



