class Hangman:
    def __init__(self):
        print "**** WELCOME TO HANGMAN GAME.... **** \n\t(1)Yes --> to START the game... \n\t(2)No -> to EXIT from the game\n"
        user_dec = raw_input("--> What you are thinking..??? ")
        if user_dec == '1':
            print "Loading the Game ...."
            self.start_game()
        elif user_dec == '2':
            print "Bye Bye..."
        else:
            print "Sorry can you repeat it again??? "
            self.__init__()

    def start_game(self):
        guess_count = 6
        secret_word = "secret"

        while guess_count > 0:
            guess_letter = raw_input("Enter you guessing letter : ")

            if guess_letter in secret_word:
                print "Wow...Guessed correct letter"
                guess_count -= 1
                secret_word = secret_word.replace(guess_letter, '', 1)
            else:
                print "Sorry...Wrong guess..Try again..."
                self.hangman_hang(guess_count)
                guess_count -= 1
            if guess_count >= 0 and len(secret_word) == 0:
                print "CONGRATS...!!! You won the Game..."
                break
            elif guess_count == 0 and len(secret_word) != 0:
                print "SOORY...You loose the Game...Guessing chance got over...."
    def hangman_hang(self, guess_count):
        if guess_count == 6:
            print "         "
            print "---------"
            print "|       |"
            print "|       0"
            print "|        "
            print "|        "
            print "|        "
        elif guess_count == 5:
            print "         "
            print "---------"
            print "|       |"
            print "|       0"
            print "|       |"
            print "|        "
            print "|        "
        elif guess_count == 4:
            print "         "
            print "---------"
            print "|       |"
            print "|       0"
            print "|      /|"
            print "|        "
            print "|        "
        elif guess_count == 3:
            print "         "
            print "---------"
            print "|       |"
            print "|       0"
            print "|      /|"
            print "|        "
            print "|        "
        elif guess_count == 2:
            print "         "
            print "---------"
            print "|       |"
            print "|       0"
            print "|      /|\\"
            print "|        "
            print "|        "
        elif guess_count == 1:
            print "         "
            print "---------"
            print "|       |"
            print "|       0"
            print "|      /|\ "
            print "|      / \\ "
            print "SORRY....!!!!You Died.. :'("
            print "Game Over....!!!"

h = Hangman()