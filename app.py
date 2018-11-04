# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.storage import SQLStorageAdapter
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = "./corpus/"

def delfile(filename):
    if os.path.exists(filename):
        os.remove(filename)

delfile("./db.sqlite3")


chatterbot = ChatBot(
    "codey",
    filters=["chatterbot.filters.RepetitiveResponseFilter"]
)
#adaptor = chatterbot.storage.SQLStorageAdapter("brain")
chatterbot.set_trainer(ChatterBotCorpusTrainer)

def train():
    print("starting to train")

    return chatterbot.train("./corpus")

train()

def clearEntry(storage):
    for x in storage.filter():
        storage.remove(x.text)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/train")
def get_train():
    return render_template("train.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatterbot.get_response(userText))

@app.route("/train-start")
def get_train_bot():
    clearEntry(chatterbot.storage)
    train()
    return redirect(url_for('home'))

@app.route('/service.yml')
def return_files_tut():
	try:
		return send_file('./corpus/service.yml', attachment_filename='service.yml')
	except Exception as e:
		return str(e)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
      return get_train_bot()


if __name__ == "__main__":
    app.run()
