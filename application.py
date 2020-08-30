#! /usr/bin/python3
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
import random
#from chatterbot.trainers import ChatterBotCorpusTrainer
from botConfig import myBotName, chatBackground, botAvatar, useGoogle, confidenceLevel

##Experimental Date Time
from dateTime import getTime, getDate

import logging
logging.basicConfig(level=logging.INFO)

application = Flask(__name__)

chatbotName = myBotName
print("Der Bot heißt: " + chatbotName)
print("Confidence level:" + str(confidenceLevel))


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
    response_selection_method=get_random_response, #Comment out um beste mögliche Antwort zu bekommen
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="botData.sqlite3"
)

bot.read_only=True #Comment out, um den Bot basierend auf Erfahrung lernen zu lassen.
print("Bot Learn Read Only:" + str(bot.read_only))

#Nach deployment des Bots bitte ausgrauen, da man den Bot nicht mehr jedes Mal trainieren muss:
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("data/trainingdata.yml")

def tryGoogle(myQuery):
	#print("<br>Du kannst gerne die Hilfe in Anspruch nehmen: <a target='_blank' href='" + j + "'>" + query + "</a>")
	return "<br><br>Du kannst gerne die Hilfe meines Freundes Google in Anspruch nehmen: <a target='_blank' href='https://www.google.com/search?q=" + myQuery + "'>" + myQuery + "</a>"

@application.route("/")
def home():
    return render_template("index.html", botName = chatbotName, chatBG = chatBackground, botAvatar = botAvatar )

@application.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    botReply = str(bot.get_response(userText))
    if botReply is "IDKresponse":
        botReply = str(bot.get_response('IDKnull')) ##Senden des I don't know befehls an den Bot
        if useGoogle == "yes":
            botReply = botReply + tryGoogle(userText)
    elif botReply == "getTIME":
        botReply = getTime()
        print(getTime())
    elif botReply == "getDATE":
        botReply = getDate()
        print(getDate())
    return botReply


if __name__ == "__main__":
    application.run()
    #application.run(host='0.0.0.0', port=80)
