#! /usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
import random
import csv
import os
from datetime import datetime
import pytz
from pytz import timezone
from chatterbot.trainers import ChatterBotCorpusTrainer
from textblob import TextBlob
## Date & Time importieren
from dateTime import getTime, getDate
from time import localtime, strftime
from time import time
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
#Einstellungen zum Chatbot:
myBotName = "Eva"
botTimeZone = "Europe/Berlin"  ##Auswahl der Zeitzone aus der vollständige Liste,welche sich unten befindet
botAvatar = "/static/Eva.png" ##Ändern des Avatars des Chatbots. Hier kann sowohl ein Bild im /static Ordner genannt werden, als auch eine URL
chatBackground = ""; ##"/static/UniKs.png"  ##Ändern des Hintergrundes hinter der Messaging Box .Hier kann sowohl ein Bild im /static Ordner genannt werden, als auch eine URL
useGoogle = "no" ## Yes - Bei nicht wissen durchsucht der Bot google nach dem unbekannten Begriff und gibt einen Link. No - Google wird nicht zur Hilfe gezogen
confidenceLevel = 0.90 ##Bot confidence level - Muss zwischen 0 und 1 liegen. Je höher der Wert, desto sicherer muss sich der Bot seiner Antwort sein



application = Flask(__name__)

chatbotName = myBotName
now = datetime.now(pytz.timezone(botTimeZone))
mm = str(now.month)
dd = str(now.day)
yyyy = str(now.year)
hour = str(now.hour)
minute = str(now.minute)
if now.minute < 10:
    minute = '0' + str(now.minute)
chatBotDate = strftime("%d.%m.%Y, %H:%M", localtime())
chatBotTime = strftime("%H:%M", localtime())


#print(strftime("%d-%m-%Y %H:%M", localtime()))
#print(strftime("%H:%M", localtime()))




print("Der Bot heißt: " + chatbotName)
print("Der Hintergrund ist:" + chatBackground)
print("Der Avatar ist: " + botAvatar)
print("Confidence level:" + str(confidenceLevel) )

#Log/ Verlauf erstellen
try:
    file = open('BotLog.csv', 'r')
    # file = open('/home/EvaluationBot/EvaluationBot/BotLog.csv', 'r')
except IOError:
    file = open('BotLog.csv', 'w')
    # file = open('/home/EvaluationBot/EvaluationBot/BotLog.csv', 'w')

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
    #input_adapter="chatterbot.input.VariableInputTypeAdapter",
    #output_adapter="chatterbot.output.OutputAdapter",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="botData.sqlite3"
)

bot.read_only=True #Comment out um den Bot basierend auf Erfahrungen lernen zu lassen.
print("Bot Learn Read Only:" + str(bot.read_only))

#Diesen Teil nach Deployment ausgrauen, um dauerhaftes Lernen zu vermeiden
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train(
    "chatterbot.corpus.english.greetings",
    "chatterbot.corpus.english.conversations",
    "data/EvaluierungsBot.yml"
)
# bot.train("/home/EvaluationBot/EvaluationBot/data/EvaluierungsBot.yml")
# bot.storage.drop()

def tryGoogle(myQuery):
	#print("<br>Gerne kannst du den Rat meines Freundes zu Hilfe ziehen: <a target='_blank' href='" + j + "'>" + query + "</a>")
	return "<br><br>Gerne kannst du die Hilfe meines Freundes Google in Anspruch nehmen: <a target='_blank' href='https://www.google.com/search?q=" + myQuery + "'>" + myQuery + "</a>"

@application.route("/", methods = ['GET'])
def home():
    return render_template("index.html")

@application.route("/getResponse", methods = ['GET'])
def get_bot_response():

    userText = str(request.args.get('msg'))
    botReply = str(bot.get_response(userText))
    sentiment = TextBlob(userText)
    sentimentScore = sentiment.sentiment.polarity
    if botReply == "IDKresponse":
        if useGoogle == "yes":
            botReply = botReply + tryGoogle(userText)
            sentimentScore = 1
    elif botReply == "getTIME":
        botReply = getTime()
        sentimentScore = 1
    elif botReply == "getDATE":
        botReply = getDate()
        sentimentScore = 1
    ##In CSV file einloggen, um Verlauf zu erstellen
    print("Open csv file")
    with open('BotLog.csv', 'a', newline='') as logFile:
    # with open('/home/EvaluationBot/EvaluationBot/BotLog.csv', 'a', newline='') as logFile:
        newFileWriter = csv.writer(logFile, delimiter = ";")
        newFileWriter.writerow([userText, botReply])
        logFile.close()
    data = {
        'botReply' : botReply,
        'sentimentScore' : sentimentScore
    }
    return jsonify(data)

@application.route("/feedback", methods = ['POST'])
def send_feedback():
    rating = request.form.get('rating')
    ux = request.form.get('ux')
    text = request.form.get('text')
    improvement = request.form.get('improve')
    with open('BotFeedback.csv', 'a', newline='') as logFile:
    # with open('/home/EvaluationBot/EvaluationBot/BotFeedback.csv', 'a', newline='') as logFile:
        newFileWriter = csv.writer(logFile, delimiter = ";")
        newFileWriter.writerow([rating, ux, text, improvement])
        logFile.close()
    return jsonify({'success':True}, 200, {'ContentType':'application/json'})

@application.route("/result", methods = ['POST'])
def send_result():
    datetime = request.form.get("datetime")
    answer1 = request.form.get("answer1")
    answer2 = request.form.get("answer2")
    answer3 = request.form.get("answer3")
    answer4 = request.form.get("answer4")
    answer5 = request.form.get("answer5")
    answer6 = request.form.get("answer6")
    with open('BotEvaluationResult.csv', 'a', newline='') as logFile:
    # with open('/home/EvaluationBot/EvaluationBot/BotEvaluationResult.csv', 'a', newline='') as logFile:
        newFileWriter = csv.writer(logFile, delimiter = ";")
        newFileWriter.writerow([datetime, answer1, answer2, answer3, answer4, answer5, answer6])
        logFile.close()

    return jsonify({'success':True}, 200, {'ContentType':'application/json'})

@application.route("/email", methods = ['POST'])
def send_email():
    email = request.form.get("email")
    with open('BotEvaluationEmail.csv', 'a', newline='') as logFile:   
    # with open('/home/EvaluationBot/EvaluationBot/BotEvaluationEmail.csv', 'a', newline='') as logFile:
        newFileWriter = csv.writer(logFile, delimiter = ";")
        newFileWriter.writerow([email])
        logFile.close()

    return jsonify({'success':True}, 200, {'ContentType':'application/json'})

if __name__ == "__main__":
    # application.run()
    application.run(host='0.0.0.0', port=80)
