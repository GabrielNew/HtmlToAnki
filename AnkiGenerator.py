import genanki
from bs4 import BeautifulSoup
from random import randint

def ReadFileHTML():
  with open("", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, 'html.parser')
  return soup

def CreateDeck():
  return genanki.Deck(deck_id = 1, name='testDeck2')
  
def CreateBasicDeckNote(question, answer):
  return genanki.Note(model=genanki.BASIC_MODEL, fields=[question, answer])

def CreateClozeDeckNote(questionAndAnswer):
  return genanki.Note(model=genanki.CLOZE_MODEL, fields=[questionAndAnswer, ''])

def AddCardDeck(deckNote):
  myDeck.add_note(deckNote)

def ExportApkgFile():
  genanki.Package(myDeck).write_to_file('testScript.apkg')

myDeck = CreateDeck()
soup = ReadFileHTML()
questionsAndAnswers = soup.find_all('ul')

for x in questionsAndAnswers:
  if(x.find('summary').find('code') == None):
    # THIS CODE IS TO CREATE A SIMPLE DECK
    question = x.find('summary').text
    answer = x.find('p').text.strip()
    deckNote = CreateBasicDeckNote(question, answer)
    AddCardDeck(deckNote)
  else:
    # THIS CODE IS TO CREATE A CLOZE DECK
    i = 1
    cs = []
    ListQa = []
    qtdAnswers = len(x.find('summary').find_all('code'))
    ListAnswers = x.find('summary').find_all('code')
    teste = str(x.find('summary'))
    ListAnswersFormated = []

    for j in range(qtdAnswers):
      index = "{{c"+str(i)+"::"
      cs.append(index)
      i+=1

    for index, element in enumerate(ListAnswers):
      formated = str(element).replace("<code>", cs[index]).replace("</code>", "}}")
      ListAnswersFormated.append(formated)
    
    for te in range(qtdAnswers):
      x.find('summary').find('code').replace_with(ListAnswersFormated[te])
    
    questionAndAnswer = str(x.find('summary').text).strip()
    deckNote = CreateClozeDeckNote(questionAndAnswer)
    AddCardDeck(deckNote)

ExportApkgFile()