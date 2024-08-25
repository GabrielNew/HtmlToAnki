import genanki
from bs4 import BeautifulSoup
from random import randint
from dotenv import load_dotenv
import os
from time import sleep

def ReadFileHTML():
  with open("", "r", encoding="utf-8") as f:
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

myDeck = CreateDeck()
soup = ReadFileHTML()
questionsAndAnswers = soup.find_all('ul', 'toggle')

for x in questionsAndAnswers:
  if(x.find('summary').find('code') != None):
    questionAndAnswer = FormatClozeDeck(x)
    deckNote = CreateClozeDeckNote(questionAndAnswer)
    AddCardDeck(deckNote)
  elif((x.find('ul') == None or x.find('ol') == None or x.find('li') == None) and x.find('p') != None):
    question = x.find('summary').text
    answer = ''
    if(len(x.find_all('p')) > 1):
      answers = x.find_all('p')
      for ans in answers:
        answer += ans.text + ' '
    else:
      answer = x.find('p').text
    print(question, answer.strip())
    deckNote = CreateBasicDeckNote(question, answer)
    AddCardDeck(deckNote)
  elif(x.find('ol') == None and x.find('ul') != None and x.find('li') != None):
    question = x.find('summary').text
    print(question)
  else:
    print(x)
    #print(x.find_all('p').text)
    #print(x.select('summary > p'))
    break

#ExportApkgFile()