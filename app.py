from flask import Flask, request, redirect, url_for, render_template, flash, jsonify, request, session
from datetime import timedelta
import json
import os
from setup import *
from handler import *

app = Flask(__name__)
app.secret_key = key

app.permanent_session_lifetime = timedelta(minutes=10)

# Password for accessing the data entry page
PASSWORD = webapppassword

# JSON file path


# Ensure the data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as file:
        json.dump([], file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        if "user" not in session:
            password = request.form['password']
            if password == PASSWORD:
                session["user"] = password
                return redirect(url_for('main'))
            else:
                flash('Incorrect password')
                return redirect(url_for('index'))
        else:
            return redirect(url_for('main'))
    else:
        session.permanent = True
        if "user" not in session:
            return render_template('index.html')
        else:
            return redirect(url_for('main'))

@app.route("/user")
def user():
    if "user" in session:
        return redirect(url_for('main'))
    else:
        return redirect(url_for("login"))

@app.route('/main',methods=['POST', "GET"])
def main():
    if "user" in session:
        return render_template('home.html')
    else:
        return redirect(url_for("login"))

@app.route('/data-entry')
def data_entry():
    if 'user' in session:
        return render_template('data_entry.html')
    else:
        return redirect(url_for('login'))

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    bday = request.form['bday']
    image_url = request.form.get('image_url', f"{display_image_url}")
    chatid = request.form.get('chatid', f"{default_chatid}")

    if not name or not bday:
        flash('Name and Birthday are required!')
        return redirect(url_for('data_entry'))

    # Set default value for image_url if it's not provided or is empty
    if not image_url:
        image_url = display_image_url
    if not chatid:
        chatid = default_chatid


    entry = {
        'name': name,
        'bday': bday,
        'image_url': image_url,
        'chatid': chatid
    }

    with open(DATA_FILE, 'r+') as file:
        data = json.load(file)
        data.append(entry)
        file.seek(0)
        json.dump(data, file, indent=4)

    return redirect(url_for('list_entries'))

@app.route('/list-entries')
def list_entries():
    if 'user' in session:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        return render_template('list_entries.html', entries=data)
    else:
        return redirect(url_for('login'))

@app.route('/delete-entry/<int:index>', methods=['POST'])
def delete_entry(index):
    if "user" in session:
        with open(DATA_FILE, 'r+') as file:
            data = json.load(file)
            if 0 <= index < len(data):
                data.pop(index)
                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=4)
        return redirect(url_for('list_entries'))
    else:
        return redirect(url_for("login"))

@app.route('/send-now', methods=['POST',"GET"])
def send_now():
    if "user" in session:
        try:
            log = checkbdays()
            delimiter = ', '
            text = delimiter.join(log)
            if(log == []):
                return render_template('display_text.html',text=" No Birthdays Today 🙄")
            else:
                return render_template('display_text.html',text=text)
        except:
            return render_template('display_text.html',text=" No Birthdays Today 🙄")
    else:
        return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
