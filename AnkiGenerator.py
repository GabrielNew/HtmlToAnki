import genanki
from bs4 import BeautifulSoup
from random import randint
from dotenv import load_dotenv
import os
from time import sleep

def ReadFileHTML():
  with open("C:\\Users\\Teste\\OneDrive\\Documents\\Programação\\Python\\AnkiFlashcardGenerator\\HTML_FLASHCARD\\testeFlashcard2.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, 'html.parser')
  return soup

def CreateDeck():
  return genanki.Deck(deck_id = 1, name='testDeck2')
  
def CreateBasicDeckNote(question, answer):
  return genanki.Note(model=genanki.BASIC_MODEL, fields=[question, answer])

def FormatClozeDeck(unformatedHtml):
  i = 1
  cs = []
  qtdAnswers = len(unformatedHtml.find('summary').find_all('code'))
  ListAnswers = unformatedHtml.find('summary').find_all('code')
  ListAnswersFormated = []

  for j in range(qtdAnswers):
    index = "{{c"+str(i)+"::"
    cs.append(index)
    i+=1

  for index, element in enumerate(ListAnswers):
    formated = str(element).replace("<code>", cs[index]).replace("</code>", "}}")
    ListAnswersFormated.append(formated)
    
  for te in range(qtdAnswers):
    unformatedHtml.find('summary').find('code').replace_with(ListAnswersFormated[te])
  
  questionWithAnswer = str(unformatedHtml.find('summary').text).strip()
  return questionWithAnswer

def CreateClozeDeckNote(questionAndAnswer):
  return genanki.Note(model=genanki.CLOZE_MODEL, fields=[questionAndAnswer, ''])

def AddCardDeck(deckNote):
  myDeck.add_note(deckNote)

def ExportApkgFile():
  genanki.Package(myDeck).write_to_file('testScript.apkg')

#load_dotenv()
#HTML_PATH = os.getenv('HTML_PATH')
#print(HTML_PATH)

total_questions = 0
myDeck = CreateDeck()
soup = ReadFileHTML()
questionsAndAnswers = soup.find_all('ul', 'toggle')

for toggle in questionsAndAnswers:
  if(toggle.find('summary').find('code') != None):
    questionAndAnswer = FormatClozeDeck(toggle)
    deckNote = CreateClozeDeckNote(questionAndAnswer)
    AddCardDeck(deckNote)
    total_questions += 1
  else:
    list_tags = []
    i = 0
    for test in toggle.find_all(True):
      if(i > 1):
        list_tags.append(test.name)
      i += 1
    list_tags = list(dict.fromkeys(list_tags))
    list_tags.remove('summary')
    if('strong' in list_tags):
      list_tags.remove('strong')
    if('p' in list_tags and (len(list_tags) == 1)):
      # JUST P TAG
      question = toggle.find('summary').text
      answer = ''
      if(len(toggle.find_all('p')) > 1):
        answers = toggle.find_all('p')
        for ans in answers:
          answer += ans.text + ' '
      else:
        answer = toggle.find('p').text
      deckNote = CreateBasicDeckNote(question, answer)
      AddCardDeck(deckNote)
    elif('li' in list_tags and (len(list_tags) == 1)):
      print('JUST LI TAG')
    elif('figure' in list_tags and (len(list_tags) == 1)):
      print('JUST FIGURE TAG')
    elif('ol' in list_tags and 'li' in list_tags and (len(list_tags) == 2)):
      print('JUST OL AND LI TAGS')
    elif('p' in list_tags and 'ul' in list_tags and 'li' in list_tags and (len(list_tags) == 3)):
      print('JUST P AND UL AND LI TAGS')
    list_tags.clear()
    
ExportApkgFile()