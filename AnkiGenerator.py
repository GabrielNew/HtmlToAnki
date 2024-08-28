import genanki
from bs4 import BeautifulSoup
from random import randint
import os
import shutil

IMAGES_PATH = r'C:\Users\Teste\OneDrive\Documents\Programação\Python\AnkiFlashcardGenerator\images'

def ReadFileHTML():
  with open("C:\\Users\\Teste\\OneDrive\\Documents\\Programação\\Python\\AnkiFlashcardGenerator\\HTML_FLASHCARD\\testeFlashcard2.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, 'html.parser')
  return soup

def CreateDeck(deckName):
  return genanki.Deck(deck_id = randint(1, 99999), name=deckName)
  
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

def ExportApkgFile(deckName):
  my_package = genanki.Package(myDeck)
  my_package.media_files = list_files(IMAGES_PATH)
  my_package.write_to_file(deckName+'.apkg')

def list_files(dir_path):
    # list to store files
    res = []
    try:
        for file_path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, file_path)):
                res.append(file_path)
    except FileNotFoundError:
        print(f"The directory {dir_path} does not exist")
    except PermissionError:
        print(f"Permission denied to access the directory {dir_path}")
    except OSError as e:
        print(f"An OS error occurred: {e}")
    return res

def copy_archives(origin, destination):
    files = os.listdir(origin)
    
    copy_files = []
    for file in files:
        origin_path = os.path.join(origin, file)
        destination_path = os.path.join(destination, file)
        if os.path.isfile(origin_path):
            shutil.copy(origin_path, destination_path)
            copy_files.append(destination_path)
    
    return copy_files

def delete_files(archives):
    for file in archives:
        if os.path.isfile(file):
            os.remove(file)
        else:
            print(f"The file {file} doesn't exist.")

soup = ReadFileHTML()
deckName = soup.find('header').text
myDeck = CreateDeck(deckName)
questionsAndAnswers = soup.find_all('ul', 'toggle')

for toggle in questionsAndAnswers:
  if(toggle.find('summary').find('code') != None):
    questionAndAnswer = FormatClozeDeck(toggle)
    deckNote = CreateClozeDeckNote(questionAndAnswer)
    AddCardDeck(deckNote)
  else:
    question = toggle.find('summary').text
    toggle.find('summary').replace_with('')
    answer = str(toggle.find('details')).replace('<details open="">', '').replace('</details>', '')
    deckNote = CreateBasicDeckNote(question, answer)
    AddCardDeck(deckNote)

copied_files = copy_archives(r'C:\Users\Teste\OneDrive\Documents\Programação\Python\AnkiFlashcardGenerator\images', r'C:\Users\Teste\OneDrive\Documents\Programação\Python\AnkiFlashcardGenerator')
ExportApkgFile(deckName.strip())
delete_files(copied_files)