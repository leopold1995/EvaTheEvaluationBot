#! /usr/bin/python3
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
import random
import csv
import os
from datetime import datetime
import pytz
from pytz import timezone
from chatterbot.trainers import ChatterBotCorpusTrainer

## Date & Time importieren
from dateTime import getTime, getDate
from time import localtime, strftime
from time import time

import logging
logging.basicConfig(level=logging.INFO)
myBotName = "Riddler"
botTimeZone = "Europe/Berlin"  ##Auswahl der Zeitzone aus der vollständige Liste,welche sich unten befindet
botAvatar = "/static/Bot2.png" ##Ändern des Avatars des Chatbots. Hier kann sowohl ein Bild im /static Ordner genannt werden, als auch eine URL
chatBackground = "/static/UniKs.png"  ##Ändern des Hintergrundes hinter der Messaging Box .Hier kann sowohl ein Bild im /static Ordner genannt werden, als auch eine URL
useGoogle = "no" ## Yes - Bei nicht wissen durchsucht der Bot google nach dem unbekannten Begriff und gibt einen Link. No - Google wird nicht zur Hilfe gezogen
confidenceLevel = 0.70 ##Bot confidence level - Muss zwischen 0 und 1 liegen. Je höher der Wert, desto sicherer muss sich der Bot seiner Antwort sein

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


print(strftime("%d-%m-%Y %H:%M", localtime()))
print(strftime("%H:%M", localtime()))




print("Der Bot heißt: " + chatbotName)
print("Der Hintergrund ist:" + chatBackground)
print("Der Avatar ist: " + botAvatar)
print("Confidence level:" + str(confidenceLevel) )

#Log/ Verlauf erstellen
try:
    file = open('BotLog.csv', 'r')
except IOError:
    file = open('BotLog.csv', 'w')

bot = ChatBot(
    "ChatBot",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
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
#bot.set_trainer(ChatterBotCorpusTrainer)
#bot.train("data/corpusmcbot.yml")

def tryGoogle(myQuery):
	#print("<br>Gerne kannst du den Rat meines Freundes zu Hilfe ziehen: <a target='_blank' href='" + j + "'>" + query + "</a>")
	return "<br><br>Gerne kannst du die Hilfe meines Freundes Google in Anspruch nehmen: <a target='_blank' href='https://www.google.com/search?q=" + myQuery + "'>" + myQuery + "</a>"

@application.route("/")
def home():
    return render_template("index.html", botName = chatbotName, chatBG = chatBackground, botAvatar = botAvatar, currentDate = chatBotDate, currentTime = chatBotTime )

@application.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    botReply = str(bot.get_response(userText))
    if botReply is "IDKresponse":
        botReply = str(bot.get_response('IDKnull')) ##Zurücksenden des I don't know befehls
        if useGoogle == "yes":
            botReply = botReply + tryGoogle(userText)
    elif botReply == "getTIME":
        botReply = getTime()
        print(getTime())
    elif botReply == "getDATE":
        botReply = getDate()
        print(getDate())
    ##In CSV file einloggen, um Verlauf zu erstellen
    print("Logge mich nun in die CSV Datei")
    with open('BotLog.csv', 'a', newline='') as logFile:
        newFileWriter = csv.writer(logFile)
        newFileWriter.writerow([userText, botReply])
        logFile.close()
    return botReply


if __name__ == "__main__":
    #application.run()
    application.run(host='0.0.0.0', port=80)
