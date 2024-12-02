from flask import Flask, request, redirect, url_for, render_template, flash, jsonify, request, session, render_template_string, send_file, abort
from datetime import timedelta
import json
import os
from setup import *
from handler import *
import getpass
from gencard import  *


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

@app.route('/gc')
def index2():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Get Username</title>
        <script>
            async function fetchUsername() {
                const response = await fetch('/get-username');
                const data = await response.json();
                document.getElementById('username').innerText = data.username;
            }
            window.onload = fetchUsername;
        </script>
    </head>
    <body>
        <h1>User Information</h1>
        <p>Username: <span id="username">Loading...</span></p>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/get-username', methods=['GET'])
def get_username():
    # Simulate getting the username from the client-side script or environment
    import os
    username = os.getenv('USERNAME') or os.getenv('USER')
    return jsonify({'username': username})

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

@app.route('/selfcheck')
def selfcheck():
    if 'user' in session:
        card_path = generate_birthday_card("RorYinBoT")
        resp = SendImgUpload("replace ur actual test message whatsapp group id here",f"./{card_path}","Test Message")
        return render_template('display_text.html',text=resp)
    else:
        return redirect(url_for('login'))

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    bday = request.form['bday']
    split_vals = bday.split("-")
    bday = f"{split_vals[0]}-{split_vals[2]}-{split_vals[1]}"
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

# Define the directory containing the images
IMAGE_DIRECTORY = "./temp"  # Path to your generated images

@app.route('/download', methods=['GET'])
def download_image():
    """
    Endpoint to download an image specified by 'filename' query parameter.
    """
    # Get the filename from the query parameters
    filename = request.args.get('filename')
    if not filename:
        abort(400, description="Filename is required.")

    # Construct the full file path
    file_path = os.path.join(IMAGE_DIRECTORY, filename)

    # Check if the file exists
    if not os.path.isfile(file_path):
        abort(404, description="File not found.")

    # Send the file for download
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
