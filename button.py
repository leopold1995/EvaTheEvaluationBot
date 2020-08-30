import pyperclip

while True:
    print('Was möchtest du auf dem Button stehen haben?:')
    linkText = input('Button Text: ')

    print('Was möchtest du als Ausgabe des Chatbots?(freilassen, um Button Text zu senden.):')
    queryText = input('Query Text: ').replace(r"'", r"\'")

    if queryText == "":
        queryText = linkText.replace(r"'", r"\'")

    newLink = '<a class=\"chatSuggest\" onclick=\"$(this).hide(); chatSuggest(\'' + queryText + '\')\";>' + linkText + '</a><br>'
    pyperclip.copy(newLink)
    print()
    print()
    print('====================================================')
    print('Kopiere diesen Code einfach in deine Antwort der chatbot.csv file:')
    print(newLink)
    print('====================================================')
    print()
    print()
