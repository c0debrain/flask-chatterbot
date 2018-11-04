from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

chatterbot = ChatBot("codey")
#chatterbot = ChatBot("codey", storage_adapter="chatterbot.storage.SQLStorageAdapter")
#chatterbot.set_trainer(ChatterBotCorpusTrainer)
#english_bot.train("chatterbot.corpus.english")
#english_bot.train("chatterbot.corpus.english")

# chatterbot.train(
#     "chatterbot.corpus.english.greetings",
#     "chatterbot.corpus.english.conversations"
# )

def train():
    chatterbot = ChatBot("codey", storage_adapter="chatterbot.storage.SQLStorageAdapter")
    chatterbot.set_trainer(ChatterBotCorpusTrainer)
    return chatterbot.train("./corpus")

train()

@app.route("/")
@app.route("/index")
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
    train()
    return redirect(url_for('index'))
    #return str("<h1>Trained! go <a href='/'>here</a> to talk to me.</h1>")

if __name__ == "__main__":
    app.run()
