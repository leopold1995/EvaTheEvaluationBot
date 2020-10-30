#! /usr/bin/python3
# -*- coding: utf-8 -*-

## Import python libraries
import random
import csv
import os
import pytz
import logging

from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ChatterBotCorpusTrainer

from pytz import timezone
from datetime import datetime
from dateTime import getTime, getDate
from time import localtime, strftime
from time import time


## Initialize Flask for webapp
app = Flask(__name__)
application = Flask(__name__)


## Application settings
logging.basicConfig(level=logging.DEBUG)
currentPath = os.path.dirname(os.path.abspath(__file__)) # Current absolute file path
logging.debug("Current path: " + currentPath)


## Flask settings
FLASK_PORT = 80 # use 8080 for local setup 


## Chatbot settings
useGoogle = "no" # Yes - Bei nicht wissen durchsucht der Bot google nach dem unbekannten Begriff und gibt einen Link. No - Google wird nicht zur Hilfe gezogen
confidenceLevel = 0.90 # Bot confidence level - Muss zwischen 0 und 1 liegen. Je höher der Wert, desto sicherer muss sich der Bot seiner Antwort sein


## Initialize dateTime util
now = datetime.now(pytz.timezone("Europe/Berlin"))
mm = str(now.month)
dd = str(now.day)
yyyy = str(now.year)
hour = str(now.hour)
minute = str(now.minute)
if now.minute < 10:
    minute = '0' + str(now.minute)
chatBotDate = strftime("%d.%m.%Y, %H:%M", localtime())
chatBotTime = strftime("%H:%M", localtime())


## Initialize ChatterBot
bot = ChatBot(
    "ChatBot",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        }
        ,{
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': confidenceLevel,
            'default_response': 'IDKresponse'
        }
    ],
    response_selection_method=get_random_response, #Art der Anwortauswahl -> random
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database=currentPath + "/database/botData.sqlite3"
)

bot.read_only=True #Comment out um den Bot basierend auf Erfahrungen lernen zu lassen.
logging.info("Bot Learn Read Only:" + str(bot.read_only))

# Diesen Teil nach Deployment ausgrauen, um dauerhaftes Lernen zu vermeiden
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations",
    currentPath + "/data/dialogues.yml"
)
# bot.storage.drop()


## Google fallback if response == IDKresponse
def tryGoogle(myQuery):
	return "<br><br>Gerne kannst du die Hilfe meines Freundes Google in Anspruch nehmen: <a target='_blank' href='https://www.google.com/search?q=" + myQuery + "'>" + myQuery + "</a>"


## CSV writer
def writeCsv(filePath, data):
    with open(filePath, "a", newline="") as logfile:
        csvWriter = csv.writer(logfile, delimiter = ";")
        csvWriter.writerow(data)


## Flask route for Eva
@application.route("/", methods = ['GET'])
def home_eva():
    return render_template("index.html")


## Flask route for eva 2.0 bot
@application.route("/eva2", methods = ['GET'])
def home_eva2():
    return render_template("eva2.html")


## Flask route for hubert bot
@application.route("/hubert", methods = ['GET'])
def home_hubert():
    return render_template("hubert.html")

## Flask route for hubert bot
@application.route("/rashid", methods = ['GET'])
def home_rashid():
    return render_template("rashid.html")


## Flask route for getting bot responses
@application.route("/getResponse", methods = ['GET'])
def get_bot_response():

    userText = str(request.args.get('msg'))
    botReply = str(bot.get_response(userText))

    if botReply == "IDKresponse":
        if useGoogle == "yes":
            botReply = botReply + tryGoogle(userText)
    elif botReply == "getTIME":
        botReply = getTime()
    elif botReply == "getDATE":
        botReply = getDate()
    
    writeCsv(currentPath + "/log/botLog.csv", [userText, botReply])

    data = {
        'botReply' : botReply
    }
    return jsonify(data)


## Flask route for posting evaluation results
@application.route("/result", methods = ['POST'])
def send_result():
    datetime = request.form.get("datetime")
    answer1 = request.form.get("answer1")
    answer2 = request.form.get("answer2")
    answer3 = request.form.get("answer3")
    answer4 = request.form.get("answer4")
    answer5 = request.form.get("answer5")
    answer6 = request.form.get("answer6")

    writeCsv(currentPath + "/log/evaluationResult.csv", [datetime, answer1, answer2, answer3, answer4, answer5, answer6])

    return jsonify({'success':True}, 200, {'ContentType':'application/json'})

## Flask route for posting evaluation results
@application.route("/resultAlternate", methods = ['POST'])
def send_result_alternate():
    bot = request.form.get("bot")
    datetime = request.form.get("datetime")
    answer1 = request.form.get("answer1")
    answer2 = request.form.get("answer2")
    answer3 = request.form.get("answer3")
    answer4 = request.form.get("answer4")
    answer5 = request.form.get("answer5")
    answer6 = request.form.get("answer6")

    writeCsv(currentPath + "/log/evaluationResultAlternate.csv", [bot, datetime, answer1, answer2, answer3, answer4, answer5, answer6])

    return jsonify({'success':True}, 200, {'ContentType':'application/json'})


## Flask route for posting feedback
@application.route("/feedback", methods = ['POST'])
def send_feedback():
    bot = request.form.get('bot')
    rating = request.form.get('rating')
    ux = request.form.get('ux')
    text = request.form.get('text')
    improvement = request.form.get('improve')

    writeCsv(currentPath + "/log/evaluationFeedback.csv", [bot, rating, ux, text, improvement])

    return jsonify({'success':True}, 200, {'ContentType':'application/json'})


## Flask route for posting email
@application.route("/email", methods = ['POST'])
def send_email():
    email = request.form.get("email")
    
    writeCsv(currentPath + "/log/evaluationEmail.csv", [email])

    return jsonify({'success':True}, 200, {'ContentType':'application/json'})


## Python Flask startup
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=FLASK_PORT)
    
