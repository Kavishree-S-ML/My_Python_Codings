"""
    HANGMAN GAME
"""

class Hangman:
    def __init__(self):
        self.r = 0

    def word_guess(self, c):
        word = "Kavishree"
        l = len(word)

        for char in word:
            if c.lower() == char and not in list:
                self.r += 1
                break
        print self.r
        if self.r == (l-1):
            return True
        return False

f = Hangman()
guess_chance = 10
while guess_chance >0:
    c = raw_input("Guessing letter: ")
    result = f.word_guess(c)
    guess_chance -= 1
    if result:
        break

if result:
    print "Congrats...!!! Right Guess :)"
else:
    print "Try Again...!!! :("