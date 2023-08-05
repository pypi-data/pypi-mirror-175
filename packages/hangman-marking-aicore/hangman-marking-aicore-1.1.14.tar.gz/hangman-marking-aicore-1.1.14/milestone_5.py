import random


class Hangman:
    '''
    Hangman is a game where the user has to guess a word by guessing the letters in the word.
    The game is over when the number of lives is 0 or the number of letters left to guess is 0.
    Parameters:
        @param word_list: a list of words to choose from
        @param num_lives: the number of lives the user has; default is 5
    Attributes:
        word: the word to guess
        word_guessed: the word with the letters guessed
        num_letters: the number of letters left to guess
        num_lives: the number of lives left
        word_list: the list of words to choose from
        list_of_guesses: the list of letters guessed
    Methods:
        check_guess: checks if the guess is in the word and updates the word_guessed
        ask_for_input: asks the user for a letter and calls the check_guess method
    '''

    def __init__(self, word_list, number_of_lives=5):
        self.word = random.choice(word_list)
        self.word_guessed = ["_" for _ in self.word]
        self.num_letters = len(set(self.word))
        self.number_of_lives = number_of_lives
        self.word_list = word_list
        self.list_of_guesses = []

    def check_guess(self, guess):
        '''
        This function checks if the letters is in the word. 
        If the letters is in the word, it replaces the "_" with the letter in the word_guessed.
        If the letter is not in the word, it subtracts 1 from the number of lives.
        Parameters: 
            @param guess: the letter guessed by the user
        '''

        guess = guess.lower()
        # Create an if statement that checks if the guess is in the word.
        if guess in self.word:
            print(f"Good guess! {guess} is in the word.")
            # Create a for loop that loops through each letter in the word
            for i, letter in enumerate(self.word):
                # Create an if statement that checks if the letter is equal to the guess
                if letter == guess:
                    # Replace the "_" with letter in the word_guessed
                    self.word_guessed[i] = letter

            self.num_letters -= 1

        else:
            self.number_of_lives -= 1
            print(f"Sorry, {guess} is not in the word.")
            print(f"You have {self.number_of_lives} lives left.")
            print(f"word guessed: {self.word_guessed}")

    def ask_for_input(self):
        '''
        This function asks the user for a letter.
        If the letter is not a single alphabetical character, it asks the user to enter a single alphabetical character.
        If the letter is already guessed, it asks the user to enter a different letter.
        If the letter is valid, it calls the check_guess method.
        '''
        while True:
            guess = input("Guess the letter: ")
            if guess.isalpha() != 1:
                print("Invalid letter. Please, enter a single alphabetical character.")
            elif guess in self.list_of_guesses:
                print("You already tried that letter!")
            else:
                # handle the logic here
                self.check_guess(guess)
                # add the guess to the list of guesses
                self.list_of_guesses.append(guess)
                break


def play_game(word_list):  # function -- this is like being external to the class
    '''
    This function plays the game.
    if the number of lives is 0, that means that the has lost the game.
    if the number of lettters is greater than 0, keep asking the user for the input
    if the number of lives is not 0 and the number of letters is not greater than 0, that means that the user has won the game.
    Parameters:
        @param word_list: a list of words to choose from
    '''
    game = Hangman(word_list, number_of_lives=5)
    while True:
        # print(f"debugging: {game.num_letters}, and {game.num_lives}")
        if game.number_of_lives == 0:
            print("You lost!")
            break
        elif game.num_letters > 0:
            game.ask_for_input()
        else:
            print("You won!")
            break

play_game(['random'])