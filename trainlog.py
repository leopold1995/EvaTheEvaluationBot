#! /usr/bin/python3

from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

#um die Daten des csv Files zu erhalten:
import os
import csv
import sys

import logging
logging.basicConfig(level=logging.INFO)

print('Möchtest du deinen Bot basierend auf den Verläufen trainieren??')
userConfirm = input('Drücke bitte y or n: ')

if(userConfirm != "y" and userConfirm != "Y"):
    print('Beginne nun mit dem Trainingsmodus')
    sys.exit()

with open('BotLog.csv') as g:
    lines = csv.reader(g)
    for line in lines:
        userText = line[0]
        botReply = line[1]
        print('##################################################')
        print('User said: ' + userText)
        print('Bot replied: ' + botReply)
        print('##################################################')
        print(' Um eine neue Antwort zu erlernen gib diese bitte ein und drücke anschließend Enter.')
        print(' Um die alte Antwort zu behalten drücke Enter.')
        print('##################################################')
        updateResponse = input('Neue Antwort: ')
        if(updateResponse != ""):
            with open('data/chatbot.csv', 'a', newline='') as logFile:
                newFileWriter = csv.writer(logFile)
                newFileWriter.writerow([userText, updateResponse])
                logFile.close()

lineCount = 0
with open('data/trainingdata.yml', 'w') as f:
    f.write("categories:\r\n")
    f.write("- Conversations")
    f.write("\r\nconversations:")
    with open('data/chatbot.csv') as g:
        lines = csv.reader(g)
        for line in lines:
            lineCount += 1
            if lineCount > 1:
                f.write("\r\n- - " + line[0])
                f.write("\r\n  - " + line[1])

print("Ich habe erfolgreich " + str(lineCount) + " Reihen importiert und werde diese nun erlernen.")

if os.path.exists("botData.sqlite3"):
    os.remove("botData.sqlite3")
    print("Lösche meinene alten Trainingsdatensatz.")

bot = ChatBot(
    "Chat Bot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="botData.sqlite3"
)

#Nach Deployment ausgrauen, da man nicht jedes Mal auf alte Trainingsdaten zugreifen möchte.
bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("data/corpus.yml")

print('##################################################')
print("Ich bin fertig mit dem Training und bereit zum Chatten!")
print("Diesen Befehl bitte auf PythonAnywhere ausführen: cp botData.sqlite3 ../botData.sqlite3")
print('##################################################')

print('Soll ich alte Verläufe löschen?')
userConfirm = input('Drücke y or n: ')

if(userConfirm != "y" and userConfirm != "Y"):
    print('Beginne nun den Trainingsmodus...')
    sys.exit()
else:
    if os.path.exists("BotLog.csv"):
        os.remove("BotLog.csv")
        print("Ich habe die alten Verläufe gelöscht.")
