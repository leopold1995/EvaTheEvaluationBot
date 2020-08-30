#! /usr/bin/python3
import urllib.request
from urllib.parse import urlparse
from os.path import splitext, basename
import os
from PIL import Image

imageURL = input("Bitte füge die URL des Bildes ein: ")

parsed = urlparse(imageURL)
root, ext = splitext(parsed.path)
imageExt = ext[1:]

print("Das ist ein " + imageExt + "Dateiformat.")

urllib.request.urlretrieve(imageURL, "avatar." + imageExt)

#Exisitert die Datei bereits?
exists = os.path.isfile('static/bot.png')

#zu png Konvertieren
if imageExt == 'png':
    ##verschieben um Avatar Datei zu ersetzen
    if exists:
        os.remove('static/bot.png')
    os.rename('avatar.png','static/bot.png')
    print('Erledigt! Dein Chatbot Avatar wurde aktualisiert.')
elif imageExt == 'jpg':
    #zu png Konvertieren
    if exists:
        os.remove('static/bot.png')
    image = Image.open('avatar.jpg')
    image.save('static/bot.png')
    os.remove('avatar.jpg')
    print('Erledigt! Dein Chatbot Avatar wurde aktualisiert.')
elif imageExt == 'gif':
    #zu png Konvertieren
    if exists:
        os.remove('static/bot.png')
    image = Image.open('avatar.gif')
    image.save('static/bot.png')
    os.remove('avatar.gif')
    print('Erledigt! Dein Chatbot Avatar wurde aktualisiert.')
else:
    os.remove("avatar." + imageExt)
    print("Mit dieser Datei konnte ich leider nichts anfangen.")
