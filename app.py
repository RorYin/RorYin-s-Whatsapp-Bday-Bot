import os
from flask.templating import render_template_string,render_template
import requests
from flask import Flask,jsonify,request,Response
from airtablehandler import *
from greenapiwrapper import *

app = Flask(__name__)



@app.route('/',methods=['POST','GET'])
def welcome():
    return "Hello, welcome to RorYin's WhatsApp Bot Webapp"

@app.route('/sendmsgurl',methods=['POST','GET'])
def todomsgurl():
    chatid=request.args.get('id')
    fileUrl=request.args.get('url')
    text= request.args.get('text')
    response = SendImgUrl(chatid,fileUrl,text)
    try:
        return response.json()
    except:
        return response

@app.route('/sendmsg',methods=['POST','GET'])
def todosendmsg():
    chatid=request.args.get('id')
    text= request.args.get('text')
    response = SendMsg(chatid,text)
    try:
        return response.json()
    except:
        return response
    
@app.route('/task',methods=['POST','GET'])
def tocheckbday():
    try:
        ToCheckIfAnyBdayToday()
        return "Checked"
    except Exception as e:
        return f"Something went wrong: {e}"


if __name__ == '__main__':
    app.debug=True
    app.run()  

