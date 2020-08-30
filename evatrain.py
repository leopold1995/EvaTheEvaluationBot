#! /usr/bin/python3
# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot(
    "ChatBot",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.90,
            'default_response': 'IDKresponse'
        }
    ],
    #response_selection_method=get_random_response, #Art der Anwortauswahl -> random
    #input_adapter="chatterbot.input.VariableInputTypeAdapter",
    #output_adapter="chatterbot.output.OutputAdapter",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="botData.sqlite3"
)

bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("./data/EvaluierungsBot.yml")