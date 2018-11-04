# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.storage import SQLStorageAdapter

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

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

if __name__ == "__main__":
    app.run()
