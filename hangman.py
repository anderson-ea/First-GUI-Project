import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.animation import Animation

Builder.load_file('hangman.kv')

WORDLIST_FILENAME = 'hangwords.txt'

#returns list of 5,000+ words
def load_words():
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.upper().split()
    return wordlist

#randomly chooses a word from word list
def choose_word(wordlist):
    return random.choice(wordlist)

#returns the word displayed on GUI
def getGuessedWord(secretWord, lettersGuessed):
    display_word = secretWord
    for y in secretWord:
        if y not in lettersGuessed:
            display_word = display_word.replace(y, '_ ')
    return display_word

allLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
wordlist = load_words()

#Widget to run the game
class MyLayout(Widget):
    lettersGuessed = []
    guessesRemaining = 6
    secretWord = choose_word(wordlist)

    #disables buttons and tells user the word they couldn't guess
    def endGame(self):
        for i in allLetters:
            self.ids[i].disabled = True
        print('you lose. the word was '+self.secretWord)

    #function to disable button after pressed
    def disable(self, button):
        button.disabled = True
        button.background_normal = ''
        button.background_color = (.7, 0.0, 0.0, .6)

    #Selects a new word and resets the board/number of guesses
    def new_word(self):
        self.secretWord = choose_word(wordlist)
        self.ids.the_word.text = getGuessedWord(self.secretWord, '')
        for i in allLetters:
            self.ids[i].disabled = False
        self.lettersGuessed = []
        self.guessesRemaining = 6

    #checks the letter guessed to see if it is in the word
    def letter_check(self, button):
        self.lettersGuessed.append(button)
        if button in self.secretWord:
            self.ids.the_word.text = str(getGuessedWord(self.secretWord, self.lettersGuessed))
            if len(self.ids.the_word.text) == len(self.secretWord):
                print('you win. press new word for new word.')
        else:
            self.guessesRemaining -= 1
            if self.guessesRemaining == 0:
                self.endGame()


class HangmanApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    HangmanApp().run()
