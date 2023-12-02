import os

# key = Fernet.generate_key()
key = "Get a key by running above line, and use same here"

airtablekey = os.environ.get('airtablekey') #"Airtable api key for ur account" #Depreciating on 1st Feb 2024,so better to use their new access token

TgBotToken = os.environ.get('TgBotToken')

devTGid = os.environ.get('devTGid')  #will be used for later implementation of error log in Telegram group as telegram apis are very reliable.

BaseId = os.environ.get('BaseId') #Change accordingly

TableId = os.environ.get('TableId') #Change accordingly

TableName = os.environ.get('TableName')  #Change accordingly

AirtableToken = os.environ.get('AirtableToken') #Change accordingly

# greenapi instance id
InstanceId = os.environ.get('InstanceId') #Change accordingly

#greenapi api token instance
ApiTokenInstance = os.environ.get('ApiTokenInstance') #Change accordingly

#deployed webapp url
webappurl = os.environ.get('webappurl') #Change accordingly