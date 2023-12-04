![](https://telegra.ph/file/b1f62ac15f2b9eca174ba.png)

 ![Adobe Photoshop](https://img.shields.io/badge/adobe%20photoshop-%2331A8FF.svg?style=for-the-badge&logo=adobe%20photoshop&logoColor=white)![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Airtable](https://img.shields.io/badge/Airtable-18BFFF?style=for-the-badge&logo=Airtable&logoColor=white)![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white) ![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)

![](https://img.shields.io/github/stars/RorYin/RorYin-s-Whatsapp-Bday-Bot.svg) ![](https://img.shields.io/github/forks/RorYin/RorYin-s-Whatsapp-Bday-Bot.svg) ![](https://img.shields.io/github/tags/RorYin/RorYin-s-Whatsapp-Bday-Bot.svg) ![](https://img.shields.io/github/release/RorYin/RorYin-s-Whatsapp-Bday-Bot.svg) ![](https://img.shields.io/github/issues/RorYin/RorYin-s-Whatsapp-Bday-Bot.svg) 





# Features
+ Can post birthday wishes on WhatsApp group chat.
+ Fun to use.
+ Its completely free of cost, hosting might cost you a minimum sum.
+ If interested you can try deploying your own using the open source code.
+ Currently deployed on render.
+ WhatsApp API from GreenAPI is use in this bot. (A great alternative to many paid APIs available).
+ Note: The free version allows 3 chats and 1000 messages per month, which is usually sufficient for a birthday bot for group with participants of 200+.

# ReleaseNote

> Currently V1.0 bot is deployed on render, can be deployed on pythonanywhere / heroku too.


# ToDo for next release
+ TBD.



# Setup for deploying your own

+ Fork the repo (better to clone the V1.0 instead of the main branch)
+ Get your api keys from GreenAPI ([green-api.com](https://green-api.com/))
+ Edit the Setup.py
	+ Create a new TG Bot using BotFather, and copy the bot token and paste it.
	+ Create a Airtable Base, and a table, with fields as "Name", "bday", "chatid".
	+ Get your Airtable access token, table id, base id and table name.
+ Choose your fav platform to deploy, recommended is pythonanywhere as it has a option to create tasks. Else you can find a way to run the Task.py at particular time.
+ Update your ENV variables once u deploy it, and restart the app.

# Airtable Guide

> Here is how to your airtable base and table should look like:
> 
![AirtableBase Example](https://telegra.ph/file/df894d1f2ec224c1f83e0.png)

# Tips

+ Deploy on pythonanywhere and set the task for Task.py to whatever time u want the bot to check and send update.
+ Use paid version of pythonanywhere to set more number of tasks if needed.


<br>

Any queries regarding deployment, contact @roryin on TG

<br><br>
_Star the repo incase if you liked it...! 😊_
